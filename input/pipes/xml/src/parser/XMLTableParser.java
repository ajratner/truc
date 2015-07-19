package parser;

import java.io.InputStream;
import java.io.FileInputStream;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/**
 * Super simple, fast StAX XML parser to grab tables from XML docs.
 **/
public class XMLTableParser {
  private InputStream xmlStream;
  private XMLInputFactory factory;
  private XMLStreamReader parser;

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
  private TableGrid parseTable(String tableId) {
    int x = -1;
    int y = -1;
    TableGrid tableGrid = new TableGrid(tableId);
    String localName;
    try {
      loop: for (int e=parser.next(); e != XMLStreamConstants.END_DOCUMENT; e = parser.next()) {
        switch (e) {
          case XMLStreamConstants.END_ELEMENT:
            localName = parser.getLocalName();
            if (parser.getLocalName().equals("table")) { break loop; }
            break;

          // TODO: ADD row/colspan!!! & TEST by adding an assert on tablegrid completeness...
          case XMLStreamConstants.START_ELEMENT:
            localName = parser.getLocalName();
            if (localName.equals("tr")) {
              y += 1;
            } else if (localName.equals("td") || localName.equals("th")) {
              x += 1;
              tableGrid.addCell(getFlatElementText(localName), x, y);
            } 
            break;
        }
      }
      return tableGrid;
    } catch (XMLStreamException ex) {
      System.out.println(ex);
      return null;
    }
  }

  /**
   * Go through the XML document, pulling out tables as TableGrid objects.
   */
  public ArrayList<TableGrid> parse() {
    HashSet<String> seenNames = new HashSet<String>();
    String docId = null;
    ArrayList<TableGrid> tableGrids = new ArrayList<TableGrid>();
    try {
      parser = factory.createXMLStreamReader(this.xmlStream);
      while (true) {
        int event = parser.next();
        if (event == XMLStreamConstants.START_ELEMENT) {
          String localName = parser.getLocalName();

          // Try to get the doc id
          if (docId == null && isDocIdSection(parser)) {
            docId = formatDocId(getFlatElementText(localName));

          // get tables
          } else if (localName.equals("table")) {
            assert docId != null;
            String tableId = docId + "." + "Table";
            if (seenNames.contains(tableId)) { tableId = iterateName(tableId); }
            seenNames.add(tableId);
            tableGrids.add(parseTable(tableId));
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

  /**
   * Number the filename.
   **/
  private String iterateName(String name) {
    Pattern p = Pattern.compile("\\d+$");
    Matcher m = p.matcher(name);
    int num = 1;
    if (m.find()) { num = Integer.parseInt(m.group()) + 1; }
    return name + "." + Integer.toString(num);
  }

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
  public XMLTableParser(InputStream xmlStream) {
    this.xmlStream = xmlStream;
    this.factory = XMLInputFactory.newInstance();
  }
}
