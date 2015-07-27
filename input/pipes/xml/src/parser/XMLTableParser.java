package parser;

import java.io.File;
import java.io.InputStream;
import java.io.FileInputStream;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.HashMap;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Super simple, fast StAX XML parser to grab tables from XML docs.
 **/
public class XMLTableParser {
  private InputStream xmlStream;
  private XMLInputFactory factory;
  private XMLStreamReader parser;
  private String fileName;
  private HashMap<String, Integer> seenNames;
  private ArrayList<TableGrid> tableGrids;

  private HashMap getElementAttributesMap() {
    HashMap<String, String> attrs = new HashMap<String, String>(); 
    for (int i=0; i < parser.getAttributeCount(); i++) {
      attrs.put(parser.getAttributeLocalName(i), parser.getAttributeValue(i));
      //System.out.println(parser.getAttributeLocalName(i) + " : " + parser.getAttributeValue(i));
    }
    return attrs;
  }

  /**
   * Extract a flat element.  See dd-genomics/parser for more complex version.
   **/
  private String getFlatElementText(String elementName) {
    StringBuilder section = new StringBuilder();
    String localName;
    try {
      loop: for (int e=parser.next(); e != XMLStreamConstants.END_DOCUMENT; e = parser.next()) {
        switch (e) {
          case XMLStreamConstants.CHARACTERS:
            section.append(parser.getText());
            break;

          case XMLStreamConstants.END_ELEMENT:
            if (parser.getLocalName().equals(elementName)) { break loop; }
            break;

          case XMLStreamConstants.START_ELEMENT:
            localName = parser.getLocalName();
            if (isSkipSection(localName)) { skipSection(localName); }
            break;
        }
      }
      return cleanup(section.toString());
    } catch (XMLStreamException ex) {
      System.out.println(ex);
      return "";
    }
  }

  /**
   * Parse an XML table into a TableGrid object.
   **/
  private TableGrid parseTable(String docId) {

    // Get tableId from docId
    assert docId != null;
    int tableNum;
    String tableId = docId + "." + "Table";
    if (seenNames.containsKey(tableId)) {
      tableNum = seenNames.get(tableId) + 1;
    } else {
      tableNum = 0;
    }
    seenNames.put(tableId, tableNum);
    tableId = tableId + "." + tableNum;

    // parse table
    int x = -1;
    int y = -1;
    int xEnd, yEnd, colspan, rowspan;
    String localName;
    HashSet<String> rowSpanPushed = new HashSet<String>();
    TableGrid tableGrid = new TableGrid(tableId);
    try {
      loop: for (int e=parser.next(); e != XMLStreamConstants.END_DOCUMENT; e = parser.next()) {
        switch (e) {
          case XMLStreamConstants.END_ELEMENT:
            localName = parser.getLocalName();
            if (parser.getLocalName().equals("table")) { break loop; }
            break;

          case XMLStreamConstants.START_ELEMENT:
            localName = parser.getLocalName();
            if (localName.equals("tr")) {
              x = -1;
              y += 1;
            } else if (localName.equals("td") || localName.equals("th")) {
              x += 1;

              // Handle some common cell attributes
              ArrayList<String> attrs = new ArrayList<String>();
              if (localName.equals("th")) { attrs.add("th"); }

              // Adjust for effect of rowspans above
              while (rowSpanPushed.contains(x+","+y)) { x += 1; }

              // Handle colspan, rowspan
              HashMap<String, String> cellAttrs = getElementAttributesMap();
              try {
                colspan = Integer.parseInt(cellAttrs.getOrDefault("colspan", "1"));
              } catch (NumberFormatException ex) {
                colspan = 1;
              }
              try {
                rowspan = Integer.parseInt(cellAttrs.getOrDefault("rowspan", "1"));
              } catch (NumberFormatException ex) {
                rowspan = 1;
              }
              xEnd = x + colspan - 1;
              yEnd = y + rowspan - 1;

              // Store the effect of rowspanning cells for cells in other rows
              for (int i=1; i < rowspan; i++) {
                for (int j=0; j < colspan; j++) {
                  rowSpanPushed.add((x+j) + "," + (y+i));
                }
              }

              // Add cell to tablegrid
              tableGrid.addCell(getFlatElementText(localName), attrs, x, xEnd, y, yEnd);
              x = xEnd;
            } 
            break;
        }
      }

      // assert basic coherence here
      assert tableGrid.isCoherent() : "Coherence error: Table " + tableId + " from file '" + fileName + "'";
      return tableGrid;
    } catch (XMLStreamException ex) {
      System.out.println(ex);
      return null;
    }
  }

  /**
   * Parse a table-wrapper (and the table within it).
   **/
  private void parseTableWrap(String docId) {
    TableGrid tableGrid = null;
    String before = null;
    String after = null;
    String localName;
    try {
      loop: for (int e=parser.next(); e != XMLStreamConstants.END_DOCUMENT; e = parser.next()) {
        switch (e) {
          case XMLStreamConstants.END_ELEMENT:
            localName = parser.getLocalName();
            if (parser.getLocalName().equals("table-wrap")) { break loop; }
            break;

          case XMLStreamConstants.START_ELEMENT:
            localName = parser.getLocalName();
            if (localName.equals("caption")) {
              before = getFlatElementText("caption"); 
            } else if (localName.equals("table-wrap-foot")) {
              after = getFlatElementText("table-wrap-foot");
            } else if (localName.equals("table")) {
              tableGrid = parseTable(docId);
            }
            break;
        }
      }
    } catch (XMLStreamException ex) {
      System.out.println(ex);
    }
    if (tableGrid != null) { 
      tableGrid.addWrapper(before, after);
      tableGrids.add(tableGrid); 
    }
  }

  /**
   * Go through the XML document, pulling out tables as TableGrid objects.
   */
  public ArrayList<TableGrid> parse() {
    String docId = null;
    try {
      parser = factory.createXMLStreamReader(this.xmlStream);
      while (true) {
        int event = parser.next();
        if (event == XMLStreamConstants.START_ELEMENT) {
          String localName = parser.getLocalName();

          // Try to get the doc id
          if (docId == null && isDocIdSection(parser)) {
            docId = formatDocId(getFlatElementText(localName));

          // if possible look for a table-wrap element (PLoS, PMC?)
          } else if (localName.equals("table-wrap")) { 
            parseTableWrap(docId);

          // get tables
          } else if (localName.equals("table")) {
            tableGrids.add(parseTable(docId));
          }
        } else if (event == XMLStreamConstants.END_DOCUMENT) {
          parser.close();
          break;
        }
      }
    } catch (XMLStreamException ex) {
      System.out.println(ex);
    }
    return tableGrids;
  }

  /**
   * PLoS / PMC: get the doc ids from the XML
   **/
  public boolean isDocIdSection(XMLStreamReader parser) {
    if (!parser.getLocalName().equals("article-id")) { return false; }
    for (int i=0; i < parser.getAttributeCount(); i++) {
      if (parser.getAttributeValue(i).equals("doi")) { return true; }
    }
    return false;
  }

  public String formatDocId(String docIdText) { return docIdText.replace("/", "."); }

  private void skipSection(String localName) {
    try {
      for (int e = parser.next(); e != XMLStreamConstants.END_DOCUMENT; e = parser.next()) {
        if (e == XMLStreamConstants.END_ELEMENT && parser.getLocalName().equals(localName)) {
          break;
        }
      }
    } catch (XMLStreamException ex) {
      System.out.println(ex);
    }
  }

  private boolean isSkipSection(String elementName) { return false; }

  private String cleanup(String x) { return x; }

  // Default constructor from InputStream
  public XMLTableParser(InputStream xmlStream, File file) {
    this.xmlStream = xmlStream;
    this.factory = XMLInputFactory.newInstance();
    this.fileName = file.getName();
    this.seenNames = new HashMap<String, Integer>();
    this.tableGrids = new ArrayList<TableGrid>();
  }
}
