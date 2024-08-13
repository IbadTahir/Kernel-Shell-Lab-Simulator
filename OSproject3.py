import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
    QWidget, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lab Manual")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        self.heading = QLabel("Lab Manual", self)
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setStyleSheet("font-size: 24px; color: #FFFFFF; background-color: #4CAF50; padding: 10px; border-radius: 10px;")
        main_layout.addWidget(self.heading)

        self.description = QLabel("To execute specific commands of the labs", self)
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet("color: #FFFFFF; font-size: 16px;")
        main_layout.addWidget(self.description)

        self.buttons = []
        for i in range(1, 9):
            button = AnimatedButton(f"Lab {i}", self)
            button.clicked.connect(lambda _, x=i: self.open_lab_window(x))
            self.buttons.append(button)
            main_layout.addWidget(button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.exit_button.clicked.connect(self.close_application)
        main_layout.addWidget(self.exit_button)

        container = QWidget()
        container.setStyleSheet("background-color: #2C3E50;")
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_lab_window(self, lab_number):
        self.lab_window = LabWindow(lab_number)
        self.lab_window.show()

    def close_application(self):
        self.close()

class LabWindow(QMainWindow):
    def __init__(self, lab_number):
        super().__init__()

        self.lab_number = lab_number
        self.setWindowTitle(f"Lab {lab_number} Commands")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        self.command_display = QTextEdit(self)
        self.command_display.setReadOnly(True)
        self.command_display.setText(self.get_lab_command(lab_number))
        self.command_display.setStyleSheet("background-color: #ECF0F1; color: #2C3E50; padding: 10px; font-family: 'Courier New'; font-size: 14px;")
        main_layout.addWidget(self.command_display)

        self.input_field = QTextEdit(self)
        self.input_field.setPlaceholderText("Enter command here...")
        self.input_field.setStyleSheet("background-color: #ECF0F1; color: #2C3E50; padding: 10px; font-family: 'Courier New'; font-size: 14px;")
        self.input_field.setFixedHeight(100)  # Adjust the height as needed
        main_layout.addWidget(self.input_field)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #ECF0F1; color: #2C3E50; padding: 10px; font-family: 'Courier New'; font-size: 14px;")
        main_layout.addWidget(self.output)

        self.allowed_commands_label = QLabel(f"Allowed commands: {', '.join(self.get_lab_allowed_commands(lab_number))}", self)
        self.allowed_commands_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        main_layout.addWidget(self.allowed_commands_label)

        button_layout = QHBoxLayout()

        self.run_input_command_button = AnimatedButton("Execute Command", self)
        self.run_input_command_button.clicked.connect(self.run_input_command)
        button_layout.addWidget(self.run_input_command_button)

        main_layout.addLayout(button_layout)

        self.back_button = AnimatedButton("Back", self)
        self.back_button.clicked.connect(self.close)
        main_layout.addWidget(self.back_button)

        container = QWidget()
        container.setStyleSheet("background-color: #34495E;")
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def get_lab_command(self, lab_number):
        commands = {
            1: "rmdir --help\nmkdir ",
            2: "dir \nquery user",
            3: """#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main()
{
  int pid;
  pid = getpid( );
  printf("Process ID is %d ",pid);
}
""",
            4: "#include <iostream>\nint main() { std::cout << \"Thread creation and matrix multiplication example\" << std::endl; return 0; }",
            5: r"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Structure to represent a process
struct Process {
    int process_id;
    int arrival_time;
    int burst_time;
};

// Function to perform First Come First Serve (FCFS) Scheduling
void FCFS(vector<Process>& processes) {
    int n = processes.size();

    // Sort processes by arrival time
    sort(processes.begin(), processes.end(), [](const Process& p1, const Process& p2) {
        return p1.arrival_time < p2.arrival_time;
    });

    // Initialize waiting time and turnaround time arrays
    vector<int> waiting_time(n);
    vector<int> turnaround_time(n);

    // Calculate waiting time for each process
    waiting_time[0] = 0;  // First process has 0 waiting time
    for (int i = 1; i < n; ++i) {
        waiting_time[i] = waiting_time[i - 1] + processes[i - 1].burst_time;
    }

    // Calculate turnaround time for each process
    for (int i = 0; i < n; ++i) {
        turnaround_time[i] = waiting_time[i] + processes[i].burst_time;
    }

    // Calculate average waiting time and average turnaround time
    double total_waiting_time = 0, total_turnaround_time = 0;
    for (int i = 0; i < n; ++i) {
        total_waiting_time += waiting_time[i];
        total_turnaround_time += turnaround_time[i];
    }
    double average_waiting_time = total_waiting_time / n;
    double average_turnaround_time = total_turnaround_time / n;

    // Display Gantt chart
    cout << "\nFCFS Scheduling Gantt Chart:\n";
    cout << "--------------------------------------------------------------\n";
    cout << "Process ID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";
    cout << "--------------------------------------------------------------\n";
    for (int i = 0; i < n; ++i) {
        cout << processes[i].process_id << "\t\t" << processes[i].arrival_time << "\t\t"
            << processes[i].burst_time << "\t\t" << waiting_time[i] << "\t\t"
            << turnaround_time[i] << endl;
    }
    cout << "--------------------------------------------------------------\n";

    // Display average waiting time and turnaround time
    cout << "\nAverage Waiting Time: " << average_waiting_time << endl;
    cout << "Average Turnaround Time: " << average_turnaround_time << endl;
}

// Example usage
int main() {
    // Example processes
    vector<Process> processes = {
        {1, 0, 4},
        {2, 1, 3},
        {3, 2, 5},
        {4, 3, 2}
    };

    // Perform FCFS scheduling
    FCFS(processes);

    return 0;
}
""",
            6: r"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Structure to represent a process
struct Process {
    int process_id;
    int arrival_time;
    int burst_time;
    int priority;
};

// Function to perform non-preemptive Priority Scheduling
void priorityNonPreemptive(vector<Process>& processes) {
    int n = processes.size();

    // Sort processes by priority (higher number means higher priority)
    sort(processes.begin(), processes.end(), [](const Process& p1, const Process& p2) {
        return p1.priority < p2.priority;
    });

    // Initialize waiting time and turnaround time arrays
    vector<int> waiting_time(n);
    vector<int> turnaround_time(n);

    // Calculate waiting time for each process
    waiting_time[0] = 0;  // First process has 0 waiting time
    for (int i = 1; i < n; ++i) {
        waiting_time[i] = waiting_time[i - 1] + processes[i - 1].burst_time;
    }

    // Calculate turnaround time for each process
    for (int i = 0; i < n; ++i) {
        turnaround_time[i] = waiting_time[i] + processes[i].burst_time;
    }

    // Calculate average waiting time and average turnaround time
    double total_waiting_time = 0, total_turnaround_time = 0;
    for (int i = 0; i < n; ++i) {
        total_waiting_time += waiting_time[i];
        total_turnaround_time += turnaround_time[i];
    }
    double average_waiting_time = total_waiting_time / n;
    double average_turnaround_time = total_turnaround_time / n;

    // Display Gantt chart
    cout << "\nNon-Preemptive Priority Scheduling Gantt Chart:\n";
    cout << "--------------------------------------------------------------\n";
    cout << "Process ID\tPriority\tBurst Time\tWaiting Time\tTurnaround Time\n";
    cout << "--------------------------------------------------------------\n";
    for (int i = 0; i < n; ++i) {
        cout << processes[i].process_id << "\t\t" << processes[i].priority << "\t\t"
            << processes[i].burst_time << "\t\t" << waiting_time[i] << "\t\t"
            << turnaround_time[i] << endl;
    }
    cout << "--------------------------------------------------------------\n";

    // Display average waiting time and turnaround time
    cout <<"\nAverage Waiting Time:" << average_waiting_time << endl;
    cout <<"Average Turnaround Time:" << average_turnaround_time << endl;
}

// Example usage
int main() {
    // Example processes
    vector<Process> processes = {
        {1, 0, 4, 2},
        {2, 1, 3, 1},
        {3, 2, 5, 3},
        {4, 3, 2, 4}
    };

    // Perform non-preemptive priority scheduling
    priorityNonPreemptive(processes);

    return 0;
}
""",
            7: r"""#include <iostream>
#include <vector>
#include <algorithm>
#include <unistd.h> // for getpid()

using namespace std;

// Structure to represent a process
struct Process {
    int process_id;
    int pid;
    int arrival_time;
    int burst_time;
};

// Function to perform Shortest Job First (SJF) Scheduling
void SJF(vector<Process>& processes) {
    int n = processes.size();

    // Sort processes by burst time
    sort(processes.begin(), processes.end(), [](const Process& p1, const Process& p2) {
        return p1.burst_time < p2.burst_time;
    });

    // Initialize waiting time and turnaround time arrays
    vector<int> waiting_time(n);
    vector<int> turnaround_time(n);

    // Calculate waiting time for each process
    waiting_time[0] = 0;  // First process has 0 waiting time
    for (int i = 1; i < n; ++i) {
        waiting_time[i] = waiting_time[i - 1] + processes[i - 1].burst_time;
    }

    // Calculate turnaround time for each process
    for (int i = 0; i < n; ++i) {
        turnaround_time[i] = waiting_time[i] + processes[i].burst_time;
    }

    // Calculate average waiting time and average turnaround time
    double total_waiting_time = 0, total_turnaround_time = 0;
    for (int i = 0; i < n; ++i) {
        total_waiting_time += waiting_time[i];
        total_turnaround_time += turnaround_time[i];
    }
    double average_waiting_time = total_waiting_time / n;
    double average_turnaround_time = total_turnaround_time / n;

    // Display Gantt chart
    cout << "\nSJF Scheduling Gantt Chart:\n";
    cout << "--------------------------------------------------------------\n";
    cout << "Process ID\tPID\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n";
    cout << "--------------------------------------------------------------\n";
    for (int i = 0; i < n; ++i) {
        cout << processes[i].process_id << "\t\t" << processes[i].pid << "\t\t"
            << processes[i].arrival_time << "\t\t" << processes[i].burst_time << "\t\t"
            << waiting_time[i] << "\t\t" << turnaround_time[i] << endl;
    }
    cout << "--------------------------------------------------------------\n";

    // Display average waiting time and turnaround time
    cout << "\nAverage Waiting Time: " << average_waiting_time << endl;
    cout << "Average Turnaround Time: " << average_turnaround_time << endl;
}

// Example usage
int main() {
    // Get the current process ID
    int pid = getpid();
    cout << "Current Process ID: " << pid << endl;

    // Example processes
    vector<Process> processes = {
        {1, pid, 0, 4},
        {2, pid + 1, 1, 3},
        {3, pid + 2, 2, 5},
        {4, pid + 3, 3, 2}
    };

    // Perform SJF scheduling
    SJF(processes);

    return 0;
}""",
            8: r"""  #include <iostream>
                    #include <fstream>
                    #include <string>

                    #define MSGSIZ 63

                        int main() {
                            std::ifstream file("year2024.txt", std::ios::in | std::ios::binary);

                            if (!file.is_open()) {
                            std::cerr << "file open failed" << std::endl;
                            return 1; // Return an error code
                            }

                        char msgbuf[MSGSIZ + 1]; // +1 for the null terminator

                     while (file) {
                     file.read(msgbuf, MSGSIZ);
                    std::streamsize bytes_read = file.gcount();

                    if (bytes_read > 0) {
                    msgbuf[bytes_read] = '\0';
                    std::cout << "message received: " << msgbuf << std::endl;
                    }
                }
                file.close();
                return 0;
                }""",
        }
        return commands.get(lab_number, "")

    def get_lab_allowed_commands(self, lab_number):
        allowed_commands = {
            1: ["rmdir", "mkdir"],
            2: ["dir", "query user"],
            3: ["gcc", "a.exe"],  # g++ and gcc, and the resulting executable a.exe
            4: ["g++", "a.exe"],  # g++ and gcc, and the resulting executable a.exe
            5: ["g++", "gcc", "a.exe"],  # g++ and gcc, and the resulting executable a.exe
            6: ["g++", "gcc", "a.exe"],
            7: ["g++", "gcc", "a.exe"],
            8: ["g++", "gcc", "a.exe"]
        }
        return allowed_commands.get(lab_number, [])

    def run_input_command(self):
        additional_command = self.input_field.toPlainText()
        if additional_command:
            if self.is_command_allowed(additional_command):
                if self.lab_number in [3, 4, 5, 6, 7, 8]:
                    cpp_code = additional_command
                    command_output = self.compile_and_run_cpp(cpp_code)
                else:
                    command_output = self.execute_command(additional_command)
                self.output.setText(command_output)
            else:
                self.output.setText("Error: Command not allowed in this lab.")
        else:
            self.output.setText("Please enter a command to run.")

    def is_command_allowed(self, command):
        allowed_commands = self.get_lab_allowed_commands(self.lab_number)
        if self.lab_number in [3, 4, 5, 6, 7, 8]:
            return True  # Allow any input for labs 3, 4, 5 (C++ code)
        return any(cmd in command for cmd in allowed_commands)

    def compile_and_run_cpp(self, cpp_code):
        try:
            # Save the C++ code to a temporary file
            cpp_file = "temp_code.cpp"
            exe_file = "temp_code.exe"
            with open(cpp_file, "w") as f:
                f.write(cpp_code)

            # Specify the path to the g++ or gcc compiler directly
            compiler_path = r"C:\MinGW\bin\g++.exe"  # Update this path to the actual path of your g++ or gcc executable

            # Check if compiler exists at the specified path
            if not os.path.exists(compiler_path):
                return f"Error: Compiler not found at {compiler_path}"

            # Print the current working directory for debugging
            cwd = os.getcwd()
            print(f"Current working directory: {cwd}")

            # Compile the C++ code
            if self.lab_number == 4:
                compile_command = f'"{compiler_path}" {cpp_file} -o {exe_file} -lpthread'  # Add -lpthread to link pthread library for lab 4
            else:
                compile_command = f'"{compiler_path}" {cpp_file} -o {exe_file}'
            print(f"Compile command: {compile_command}")
            compile_output = subprocess.getoutput(compile_command)
            print(f"Compile output: {compile_output}")

            if "error" in compile_output.lower():
                return f"Compilation Error:\n{compile_output}"

            # Check if the executable was created
            if not os.path.exists(exe_file):
                return "Compilation failed: temp_code.exe not created."

            # Run the compiled program
            run_command = f".\\{exe_file}"
            run_output = subprocess.getoutput(run_command)
            print(f"Run command: {run_command}")
            print(f"Run output: {run_output}")
            return run_output
        except Exception as e:
            return str(e)

    def execute_command(self, command):
        try:
            command_output = subprocess.getoutput(command)
            custom_output = self.customize_output(command, command_output)
            return custom_output
        except Exception as e:
            return str(e)

    def customize_output(self, command, original_output):
        if "mkdir" in command:
            return "Directory created successfully.\n" + original_output
        elif "rmdir" in command:
            return "Directory removed successfully.\n" + original_output
        elif "ls" in command:
            return "List of directory contents:\n" + original_output
        elif "pwd" in command:
            return "Current working directory:\n" + original_output
        elif "echo" in command:
            return original_output
        else:
            return original_output

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
