#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

#include "func_utils.hpp"

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <filename> <io_type> <round>\n";
        return 1;
    }

    std::string io_type(argv[2]);
    std::string round(argv[3]);
    size_t num_round = std::stoi(round);

    std::ifstream file(argv[1]);
    if (!file) {
        std::cerr << "Unable to open file: " << argv[1] << std::endl;
        return 1;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string contents = buffer.str();
    file.close();
    auto body = llama_functionary::json::parse(contents);

    if (io_type.compare("0") == 0) {    
        llama_functionary::generate_oai_messages(body);
        auto messages = body["messages"];
        if (messages.size() <= num_round) {
            std::cerr << "Invalid round number: " << num_round << std::endl;
            return 1;
        }
        std::cout << messages[num_round]["content"].get<std::string>();
    } else {
        llama_functionary::convert_oai_response(body);
        std::cout << body.dump_style();
    }

    return 0;
}

