  #include <iostream>
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
                }