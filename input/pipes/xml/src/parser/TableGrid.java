package parser;

import java.util.ArrayList;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class TableGrid {
  private String id;
  private ArrayList<String> cellContents;
  private ArrayList<int[]> cellCoordinates;
  private ArrayList<ArrayList<String>> cellAttributes;
  private ArrayList<String> cellTypes;

  public void addCell(String content, String type, ArrayList<String> attrs, int xs, int xe, int ys, int ye) {
    cellContents.add(content);
    cellTypes.add(type);
    cellAttributes.add(attrs);
    int[] coords = new int[4];
    coords[0] = xs;
    coords[1] = xe;
    coords[2] = ys;
    coords[3] = ye;
    cellCoordinates.add(coords);
  }
  public void addCell(String content, String type, ArrayList<String> attrs, int xs, int ys) {
    addCell(content, type, attrs, xs, xs, ys, ys);
  }

  /**
   * Check to see if table has been captured correctly.  Anything actually worth putting here?
   **/
  public boolean isCoherent() {
    return true;
  }

  private String escapeTSV(String x) {
    if (x == null) { return "\\N"; }
    return x.replace("\n", " ").replace("\t", " ").replace("\\", "\\\\");
  }

  private String escapeTSV(String[] x) {
    if (x == null) { return "\\N"; }
    StringBuilder list = new StringBuilder();
    list.append("{");
    for (int i = 0; i < x.length; i++) {
      list.append("\"");
      list.append(x[i].replace("\\", "\\\\\\\\").replace("\"", "\\\\\""));
      list.append("\"");
      if (i < x.length - 1) { list.append(","); }
    }
    list.append("}");
    return list.toString();
  }

  private String escapeTSV(ArrayList<String> x) {
    if (x == null) { return "\\N"; }
    String[] xArr = new String[x.size()];
    xArr = x.toArray(xArr);
    return escapeTSV(xArr);
  }
  
  private String escapeTSV(int[] x) {
    if (x == null) { return "\\N"; }
    StringBuilder list = new StringBuilder();
    list.append("{");
    for (int i = 0; i < x.length; i++) {
      list.append(x[i]);
      if (i < x.length - 1) { list.append(","); }
    }
    list.append("}");
    return list.toString();
  }

  public String toTSV() {
    StringBuilder s = new StringBuilder();
    for (int i = 0; i < cellContents.size(); i++) {

      // Table ID
      s.append(id);
      s.append("\t");
      
      // Cell ID
      s.append(i);
      s.append("\t");
      
      // Cell content
      // TODO: put string splitting somewhere else?
      String[] cellWords = null;
      if (cellContents.get(i) != null) {
        cellWords = cellContents.get(i).split("\\s+");
      }
      s.append(escapeTSV(cellWords));
      s.append("\t");
      
      // Cell types
      s.append(cellTypes.get(i));
      s.append("\t");

      // Cell attributes
      if (cellAttributes.get(i) != null && cellAttributes.get(i).size() > 0) {
        s.append(escapeTSV(cellAttributes.get(i)));
      } else {
        s.append("\\N");
      }
      s.append("\t");

      // Cell coordinates- print out as X, X_SPAN (rather than X_START, X_END)
      // TODO: make this convention uniform throughout so as not to be confusing
      int[] coords = cellCoordinates.get(i);
      s.append(coords[0]);
      s.append("\t");
      s.append(coords[1] - coords[0]);
      s.append("\t");
      s.append(coords[2]);
      s.append("\t");
      s.append(coords[3] - coords[2]);

      s.append("\n");
    }
    return s.toString();
  }

  public JSONObject toJSON() {
    JSONObject tableGrid = new JSONObject();
    tableGrid.put("id", id);
    JSONArray cells = new JSONArray();
    for (int i = 0; i < cellContents.size(); i++) {
      JSONObject cell = new JSONObject();

      // Content
      cell.put("c", cellContents.get(i));

      // Attributes
      if (cellAttributes.get(i).size() > 0) {
        JSONArray attrs = new JSONArray();
        for (String attr : cellAttributes.get(i)) { attrs.add(attr); }
        cell.put("attrs", attrs);
      }

      // Coordinates- compressed format
      int[] coords = cellCoordinates.get(i);
      if (coords[0] == coords[1]) {
        cell.put("x", coords[0]);
      } else {
        JSONArray xs = new JSONArray();
        xs.add(coords[0]);
        xs.add(coords[1]);
        cell.put("x", xs);
      }
      if (coords[2] == coords[3]) {
        cell.put("y", coords[2]);
      } else {
        JSONArray ys = new JSONArray();
        ys.add(coords[2]);
        ys.add(coords[3]);
        cell.put("y", ys);
      }
      cells.add(cell);
    }
    tableGrid.put("cells", cells);
    return tableGrid;
  }

  public String toJSONString() { return toJSON().toJSONString(); }

  public TableGrid(String id) {
    this.id = id;
    this.cellContents = new ArrayList<String>();
    this.cellTypes = new ArrayList<String>();
    this.cellCoordinates = new ArrayList<int[]>();
    this.cellAttributes = new ArrayList<ArrayList<String>>();
  }
}
