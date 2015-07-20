package parser;

import java.util.ArrayList;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class TableGrid {
  private String id;
  private ArrayList<String> cellContents;
  private ArrayList<int[]> cellCoordinates;

  public void addCell(String content, int xs, int xe, int ys, int ye) {
    cellContents.add(content);
    int[] coords = new int[4];
    coords[0] = xs;
    coords[1] = xe;
    coords[2] = ys;
    coords[3] = ye;
    cellCoordinates.add(coords);
  }
  public void addCell(String content, int xs, int ys) {
    addCell(content, xs, xs, ys, ys);
  }

  /**
   * Check to see if table has been captured correctly.
   **/
  public boolean isCoherent() {
    int d = cellCoordinates.size();
    int[] rowMaxs = new int[d];
    int[] colMaxs = new int[d];
    for (int[] coords : cellCoordinates) {
      if (rowMaxs[coords[3]] < coords[1]) { rowMaxs[coords[3]] = coords[1]; }
      if (colMaxs[coords[1]] < coords[3]) { colMaxs[coords[1]] = coords[3]; }
    }
    int rowMaxFirst = rowMaxs[0];
    int colMaxFirst = colMaxs[0];
    for (int i=0; i < d; i++) {
      if (rowMaxs[i] > 0 && rowMaxs[i] != rowMaxFirst) { return false; }
      if (colMaxs[i] > 0 && colMaxs[i] != colMaxFirst) { return false; }
    }
    return true;
  }

  public JSONObject toJSON() {
    JSONObject tableGrid = new JSONObject();
    tableGrid.put("id", id);
    JSONArray cells = new JSONArray();
    for (int i = 0; i < cellContents.size(); i++) {
      JSONObject cell = new JSONObject();

      // Content
      cell.put("content", cellContents.get(i));

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
    this.cellCoordinates = new ArrayList<int[]>();
  }
}
