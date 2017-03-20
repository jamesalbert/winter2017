// Al Gore Invented The Internet

import com.mesquite.csim.*;
import com.mesquite.csim.Process;
import com.mesquite.csim.file.Files;
import java.io.*;

public class TrainSimulator extends Model {
  private static double simTime, mu;
  private static double dockbusy, dockhogged, dockidle = 0;
  private FCFSFacility dock;
  public Event NotInUse, Idle, NotIdle;
  public Table TimeInQueue, TimeInSystem, TimeDockBusy,
               TimeDockHogged, TimeDockIdle,
               HoggedOutTrains;
  public QTable TrainsInQueue;

  public static void main(String args[]) {
    simTime = args.length >= 1 ? Double.parseDouble(args[0]) : 7200;
    mu = args.length >= 2 ? Double.parseDouble(args[1]) : 10;
    TrainSimulator model = new TrainSimulator();
    model.enableTrace(true);
    model.run();
    model.report();
    double dockbusyperc = (dockbusy / simTime) * 100;
    double dockhoggedperc = (dockhogged / simTime) * 100;
    double dockidleperc = (dockidle / simTime) * 100;
    double docktimeperc = dockbusyperc + dockhoggedperc + dockidleperc;

    String DockMessage = String.format(
      "Time Dock was Busy: %1$f%%\n" +
      "Time Dock was Hogged: %2$f%%\n" +
      "Time Dock was Idle: %3$f%%\n" +
      "With a total of %4$f%%",
      dockbusyperc,
      dockhoggedperc,
      dockidleperc,
      docktimeperc
    );
    System.out.println(DockMessage);
  }

  public TrainSimulator() {
    super("TrainSimulator");
  }

  public void run() {
    start(new Sim());
  }

  private class Sim extends Process {
    public Sim() {
      super("Sim");
    }

    public void run() {
      rand.setSeed(10);
      dock = new FCFSFacility("Dock", 1);
      NotInUse = new Event("NotInUse");
      NotIdle = new Event("NotIdle");
      Idle = new Event("Idle");
      add(new IdleChecker());
      Idle.set();
      add(new TrainGenerator());
      hold(simTime);
    }
  }

  private class TrainGenerator extends Process {
    public TrainGenerator() {
      super("TrainGenerator");
      TimeInQueue = new Table("Time in Queue");
      TimeInSystem = new Table("Time in System");
      TimeDockBusy = new Table("Time Dock was Busy");
      TimeDockHogged = new Table("Time Dock was Hogged");
      TimeDockIdle = new Table("Time Dock was Idle");
      TimeInSystem.confidence();
      TimeInQueue.setPermanent(true);
      TimeDockBusy.setPermanent(true);
      TimeDockHogged.setPermanent(true);
      TimeDockIdle.setPermanent(true);
      TimeInSystem.setPermanent(true);
      TrainsInQueue = new QTable("Number of Trains in Queue");
      TrainsInQueue.setPermanent(true);
      HoggedOutTrains = new Table("Hogged Out Trains");
      HoggedOutTrains.add_histogram(5, 0, 5);
    }

    public void run() {
      NotInUse.set();
      while(true) {
        add(new Train());
        hold(rand.exponential(mu));
      }
    }
  }

  private class Train extends Process {
    Crew crew;
    Event hogout = new Event("Hogout");
    Event hogin = new Event("Hogin");
    int hogouts = 0;

    public Train() {
      super("Train");
    }

    public void run() {
      double arrived_in_system, arrived_in_queue,
             departed_from_system, departed_from_queue,
             service_time, time_left, start, end,
             time_in_system, time_in_queue,
             next_hogout;
      arrived_in_system = clock();
      new_crew();
      arrived_in_queue = clock();
      TrainsInQueue.note_entry();
      while (!NotInUse.timed_queue(crew.get_next_hogout())) {
        hogouts++;
        hogin.untimed_wait();
        new_crew();
      }
      TrainsInQueue.note_exit();
      NotIdle.set();
      departed_from_queue = clock();
      time_in_queue = departed_from_queue - arrived_in_queue;
      Event done = new Event("End Service");
      TimeInQueue.record(time_in_queue);
      dock.reserve();
      service_time = rand.uniform(3.5, 4.5);
      time_left = service_time;
      next_hogout = crew.get_next_hogout();
      while (time_left > next_hogout) {
        hold(next_hogout);
        TimeDockBusy.record(next_hogout);
        dockbusy += next_hogout;
        start = clock();
        hogout.untimed_wait();
        hogouts++;
        hogin.untimed_wait();
        new_crew();
        end = clock();
        TimeDockHogged.record(end - start);
        dockhogged += end - start;
        time_left -= next_hogout;
        next_hogout = crew.get_next_hogout();
      }
      hold(time_left);
      TimeDockBusy.record(time_left);
      dockbusy += time_left;
      dock.release();
      NotInUse.set();
      departed_from_system = clock();
      time_in_system = departed_from_system - arrived_in_system;
      TimeInSystem.record(time_in_system);
      HoggedOutTrains.record(hogouts);
      Idle.set();
    }

    public void new_crew() {
      crew = new Crew(hogout, hogin);
      add(crew);
      hold(0);
    }
  }

  private class Crew extends Process {
    Event hogout, hogin;
    double time;
    double start;
    public Crew(Event ho, Event hi) {
      super("Crew");
      hogout = ho;
      hogin = hi;
      start = clock();
    }

    public void run() {
      time = rand.uniform(6, 11);
      hold(time);
      hogout.set();
      hold(rand.uniform(2.5, 3.5));
      hogin.set();
    }

    public double get_next_hogout() {
      return (start + time) - clock();
    }
  }

  private class IdleChecker extends Process {
    double start, end;
    public IdleChecker() {
      super("Idle Checker");
    }

    public void run() {
      while (true) {
        Idle.untimed_wait();
        start = clock();
        NotIdle.untimed_wait();
        end = clock();
        TimeDockIdle.record(end - start);
        dockidle += end - start;
      }
    }
  }
}
