package parser;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.util.ArrayList;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class Main {

  public static void main(String[] args) {
    if (args.length != 1) {
      System.out.println("Usage: java -ea -jar parser.jar [XML_FILES_DIR]");
      System.exit(0);
    }

    ArrayList<File> files = getAllFiles(args[0]);

    try {
      for (File file : files) {
        InputStream xmlInput = new FileInputStream(file);
        XMLTableParser parser = new XMLTableParser(xmlInput);
        for (TableGrid tableGrid : parser.parse()) {
          System.out.println(tableGrid.toJSONString());
        }
      }
    } catch (Throwable err) {
      err.printStackTrace();
      System.exit(0);
    }
  }

  public static void addAllFiles(ArrayList<File> files, File file) {
    if (file.isFile()) {
      files.add(file);
    } else if (file.isDirectory()) {
      for (File f : file.listFiles()) { addAllFiles(files, f); }
    }
  }

  public static ArrayList<File> getAllFiles(String path) {
    ArrayList<File> files = new ArrayList<File>();
    File file = new File(path);
    assert file.exists();
    addAllFiles(files, file);
    return files;
  }
}
