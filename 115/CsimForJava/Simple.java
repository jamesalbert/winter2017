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
                add(new Job());
                hold(rand.exponential(10));
            }
        }
    }

    private class Job extends Process {
        public Job() {
            super("Job");
        }

        public void run() {
            while (true) {
                double remaining_time = rand.uniform(6, 11);
                double service_time = rand.uniform(3.5, 4.5);
                if (m_fac.timed_reserve(remaining_time) == -1)
                    continue;
                hold(service_time);
                m_fac.release();
            }
        }
    }
}
