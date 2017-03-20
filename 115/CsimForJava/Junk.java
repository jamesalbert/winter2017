// Statistics can eat my cock

import com.mesquite.csim.*;
import com.mesquite.csim.Process;
import com.mesquite.csim.file.Files;
import java.io.*;

public class Simple extends Model {
  private static final double simTime = 7200.00;
  private static final double iarTime = 10.0;
  private static final double srvTime = 1.0;
  private FCFSFacility m_fac;

  public static void main(String args[]) {
    Simple model = new Simple();
    model.enableTrace(true);
    model.run();
    model.report();
  }

  public Simple() {
    super("Simple");
  }

  public void run() {
    start(new Sim());
  }

  private class Sim extends Process {
    public Sim() {
      super("Sim");
    }

    public void run() {
      m_fac = new FCFSFacility("fac", 1);
      add(new Gen());
      hold(simTime);
    }
  }

  private class Gen extends Process {
    public Gen() {
      super("Gen");
    }

    public void run() {
      while(true) {
        add(new Train());
        hold(rand.exponential(10));
      }
    }
  }

  private class Train extends Process {
    public Train() {
      super("Train");
    }

    public void run() {
      double remaining_time = rand.uniform(6, 11);
      double service_time = rand.uniform(3.5, 4.5);
      System.out.println(remaining_time);
      Event hogout = new Event("Hogout");
      Event serviced = new Event("Serviced");
      Event[] events = {hogout, serviced};
      EventSet updates = new EventSet("events", events);
      Process HogoutProc = new Hogout(hogout, remaining_time);
      Service ServiceProc = new Service(serviced, service_time);
      add(HogoutProc);
      add(ServiceProc);

      for (int i = 0; i < m_fac.process_list().size(); i++) {
        Object proc = m_fac.process_list().get(i);
        System.out.println(proc);
      }

      //double hogout_time = clock() + remaining_time;
      //System.out.println(now);
      int tindex = updates.wait_any();
      Event triggered = updates.get(tindex);
      if (triggered.name() == "Hogout") {
        // handle hogout
        double clock_in = rand.uniform(2.5, 3.5);
        ServiceProc.hold(clock_in);
      } else {
        // handle serviced
      }
    }
  }

  private class Service extends Process {
    Event event;
    double time;
    double interval;
    public Service(Event e, double t) {
      /*
      Event e - serive ended event
      double t - time until
      */
      super("Service");
      event = e;
      time = t;
      interval = t;
    }

    public void run() {
      // m_fac.use(time);
      m_fac.reserve();
      hold(time);
      m_fac.release();
      event.set();
    }
  }

  private class Hogout extends Process {
    Event event;
    double time;
    public Hogout(Event e, double t) {
      /*
      Event e - hogout event
      double t - time until
      */
      super("Hogout");
      event = e;
      time = t;
    }

    public void run() {
      hold(time);
      event.set();
    }
  }
}
