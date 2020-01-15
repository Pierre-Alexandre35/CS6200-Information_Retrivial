import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Driver {

  public static void main(String[] args) throws IOException {
    File[] files = new File("./assets/student-1").listFiles();
    Generator gene = new Generator(files);
    HashMap<Path, List<String>> result = gene.getEveryWords();
    Analyze sampleOne = new Analyze(result);
    sampleOne.findAll("kill");
  }

}
