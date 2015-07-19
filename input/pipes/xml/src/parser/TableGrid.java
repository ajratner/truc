package parser;

import java.util.ArrayList;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class TableGrid {
  private String id;
  private ArrayList<String> cellContents;
  private ArrayList<Integer[]> cellCoordinates;

  public void addCell(String content, int xs, int xe, int ys, int ye) {
    cellContents.add(content);
    Integer[] coords = new Integer[4];
    coords[0] = xs;
    coords[1] = xe;
    coords[2] = ys;
    coords[3] = ye;
    cellCoordinates.add(coords);
  }
  public void addCell(String content, int xs, int ys) {
    addCell(content, xs, xs, ys, ys);
  }

  public JSONObject toJSON() {
    JSONObject tableGrid = new JSONObject();
    tableGrid.put("id", id);
    JSONArray cells = new JSONArray();
    for (int i = 0; i < cellContents.size(); i++) {
      JSONObject cell = new JSONObject();
      cell.put("content", cellContents.get(i));
      cell.put("x-start", cellCoordinates.get(i)[0]);
      cell.put("x-end", cellCoordinates.get(i)[1]);
      cell.put("y-start", cellCoordinates.get(i)[2]);
      cell.put("y-end", cellCoordinates.get(i)[3]);
      cells.add(cell);
    }
    tableGrid.put("cells", cells);
    return tableGrid;
  }

  public String toJSONString() { return toJSON().toJSONString(); }

  public TableGrid(String id) {
    this.id = id;
    this.cellContents = new ArrayList<String>();
    this.cellCoordinates = new ArrayList<Integer[]>();
  }
}
