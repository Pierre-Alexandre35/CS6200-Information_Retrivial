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

  public int getTermFrequency(String search){
    int count = 0;
    for(Map.Entry<Path, List<String>> entry : input.entrySet()){
      for(String item : entry.getValue()){
        System.out.println(entry.getKey() + ": " + item);
        if(item.contains(search)){
          count ++;
        }
      }
    }
    System.out.println(count);
    return 1;
  }

  public void getTermFrequencyLists(Path givenPath){
    HashMap<String, Integer> frequencyMap = new HashMap<>();

    for(String value : input.get(givenPath)){
      int count = 1;
      if(frequencyMap.containsKey(value)){
        int temp = frequencyMap.get(value);
        count = temp + 1;
      }
      frequencyMap.put(value,count);



    }
    System.out.println(frequencyMap.entrySet());

  }

  private void getMatches(String search){

  }

}
