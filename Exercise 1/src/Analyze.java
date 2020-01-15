import java.nio.file.Path;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class Analyze {
  HashMap<Path, List<String>> input;

  Analyze(HashMap<Path, List<String>> input){
    this.input = input;
  }

  public int findAll(String search){
    for(Map.Entry<Path, List<String>> entry : input.entrySet()){
      for(String item : entry.getValue()){
        System.out.println(entry.getKey() + ": " + item);
      }
    }
    return 1;
  }

  private void getMatches(String search){

  }

}
