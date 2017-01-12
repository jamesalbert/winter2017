import com.mesquite.csim.*;
import com.mesquite.csim.Process;
import com.mesquite.csim.file.Files;
import java.io.*;

public class App extends Model {
    public static void main(String args[]) {
    App model = new App();
    m_s = Files.Setfile("App.out");
    model.setOutputStream(m_s);
    model.run();
    model.report();
    }
    public App() {
        super("App");
    }
    public void run() {
        start(new Sim());
    }
    private static final double simTime = 10000.0;
    private static final double iarTime = 2.0;
    private static final double srvTime = 1.0;
    private FCFSFacility m_fac;
    private static PrintStream m_s;
}
