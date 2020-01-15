import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

public class Driver {

  public static void main(String[] args) throws IOException {
      File fileOne = new File("./assets/homework1");
      String st ="";
      try{
        BufferedReader reader = new BufferedReader(new FileReader(fileOne));
        st = reader.readLine();
      }catch(IOException e){
        System.out.println("An error occurs");
      }
      List generatorOne = new Generator(st).toArray();
  }

}
