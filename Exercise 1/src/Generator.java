import java.util.LinkedList;
import java.util.List;

public class Generator {
  String text;
  Generator(String text){
    this.text = text;
  }

  List toArray(){
    List<String> result = new LinkedList<>();
    String[] old = text.split(" ");
    for(int i = 0 ; i < old.length ; i++){
      result.add(old[i]);
    }
    return result;
  }
}
