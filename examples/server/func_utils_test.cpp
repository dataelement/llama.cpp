#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

#include "func_utils.hpp"

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <filename> <io_type> <system_or_user>\n";
        return 1;
    }

    std::string io_type(argv[2]);
    std::string system_or_user(argv[3]);

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
        llama_functionary::adapte_oai_with_tool_call(body);
        auto messages = body["messages"];
        if (system_or_user.compare("1") == 0) {
            std::cout << messages[0]["content"];
        } else {
            std::cout << messages[1]["content"];
        }   
    } else {
        llama_functionary::convert_response_to_oai_choices(body);
        std::cout << body.dump_style();
    }

    return 0;
}

