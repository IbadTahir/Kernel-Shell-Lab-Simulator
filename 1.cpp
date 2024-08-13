#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Process {
    int pid;        // Process ID
    int arrival;    // Arrival time
    int burst;      // Burst time
};

void fcfs(vector<Process>& processes) {
    sort(processes.begin(), processes.end(), [](const Process& p1, const Process& p2) {
        return p1.arrival < p2.arrival; // Sort processes by arrival time
    });

    int n = processes.size();
    int total_turnaround = 0, total_waiting = 0;
    int current_time = 0;

    cout << "Process\t Arrival\t Burst\t Completion\t Turnaround\t Waiting\n";
    for (int i = 0; i < n; ++i) {
        current_time = max(current_time, processes[i].arrival); // Process arrives or waits until previous process completes
        int completion_time = current_time + processes[i].burst;
        int turnaround_time = completion_time - processes[i].arrival;
        int waiting_time = turnaround_time - processes[i].burst;

        total_turnaround += turnaround_time;
        total_waiting += waiting_time;

        cout << processes[i].pid << "\t\t " << processes[i].arrival << "\t\t " << processes[i].burst
             << "\t\t " << completion_time << "\t\t " << turnaround_time << "\t\t " << waiting_time << "\n";

        current_time = completion_time; // Update current time to the completion time of the current process
    }

    double avg_turnaround = (double)total_turnaround / n;
    double avg_waiting = (double)total_waiting / n;

    cout << "\nAverage Turnaround Time: " << avg_turnaround << endl;
    cout << "Average Waiting Time: " << avg_waiting << endl;
}

int main() {
    int n;
    cout << "Enter the number of processes: ";
    cin >> n;

    vector<Process> processes(n);

    cout << "Enter arrival time and burst time for each process:\n";
    for (int i = 0; i < n; ++i) {
        processes[i].pid = i + 1;
        cout << "Process " << processes[i].pid << " Arrival time: ";
        cin >> processes[i].arrival;
        cout << "Process " << processes[i].pid << " Burst time: ";
        cin >> processes[i].burst;
    }

    fcfs(processes);

    return 0;
}
