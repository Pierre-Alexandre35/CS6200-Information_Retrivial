import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Generator {
  File[] files;

  Path pathFileOne = Paths.get("/Users/Pierre-Alexandre/Documents/Classes/Information Retrivial/Exercise 1/./assets/student-1/episode4");

  Generator(File[] files){
    this.files = files;
  }

  public HashMap<Path, List<String>> getEveryWords () throws IOException {
    HashMap<Path, List<String>> result = new HashMap<>();
    for(File file : files){
      Scanner fileScan = new Scanner(new File(String.valueOf(file)));
      List<String> fileWords = new LinkedList<>();
      while(fileScan.hasNext()){
        String strippedInput = fileScan.next().replaceAll("\\W", "");
        fileWords.add(strippedInput);
      }
      result.put(Paths.get(file.getAbsolutePath()),fileWords);
    }
    return result;
  }
}
