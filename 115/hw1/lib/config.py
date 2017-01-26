conf = {
    'arrival': 'Time {time:.2f}: train {train.id} arrival for {train.unload_time:.2f}h of unloading; crew {train.id} with {train.crew.hours_left:.2f}h before hogout',
    'enter-queue': 'Time {time:.2f}: train {train.id} entering queue',
    'start-service': 'Time {time:.2f}: train {train.id} starting service lasting {train.unload_time:.2f}h',
    'end-service': 'Time {time:.2f}: train {train.id} ending service',
    'exit-queue': 'Time {time:.2f}: train {train.id} leaving queue',
    'departure': 'Time {time:.2f}: train {train.id} is departing',
    'hogout': 'Time {time:.2f}: train {train.id}\'s crew has hogged out. Next crew arrives in {train.crew.until_arrival:.2f}h',
    'hogin': 'Time {time:.2f}: train {train.id}\'s new crew has just arrived with {train.crew.hours_left:.2f}h before hogout',
    'stats': '--- Stats\ntrains served: {served}\naverage time train is in system: {avg_time:.2f}h\nmax time train is in system: {max_time:.2f}h\ntotal dock idle: {idle:.2f}%\ntotal dock busy: {busy:.2f}%\ntotal dock hogged-out: {hogged_out:.2f}%\nmaximum # trains in queue: {max_queue} trains\naverage time in queue: {avg_queue:.2f}h'
}

schema = {
    'stats': {
        'served': int(),
        'trains': dict(),
        'start_service': float(),
        'end_service': float(),
        'start_hogout': float(),
        'max_time': int(),
        'avg_time': float(),
        'avg_queue': float(),
        'max_queue': int(),
        'queue': dict(),
        'busy': float(),
        'idle': float(),
        'hogged_out': float(),
        'final_time': float()
    }
}
