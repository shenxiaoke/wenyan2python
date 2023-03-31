import re
from pycnnum import cn2num

class wenyan(object):

    def __init__(self,lines):
        self.string = lines.split('\n')
        self.english_name_num = 0
        self.c2e_dict = {}

    def c2e(self,chinese_name):
        if chinese_name in self.c2e_dict:
            return self.c2e_dict[chinese_name]
        self.english_name_num += 1
        self.c2e_dict[chinese_name] = 'a'+str(self.english_name_num)
        return self.c2e_dict[chinese_name] 

    def wenyan2python(self):
        python_code = ""

        in_loop = 0 #depth of loop

        for line in self.string:

            while line:
                # print(line)

                loop_match = re.search(r"为是「(\S+?)」遍。",line)
                num_match = re.search(r"吾有一数，曰「(\S+?)」。名之曰「(\S+?)」。",line)
                string_match = re.search(r"吾有一言。曰「「(\S+?)」」。书之。",line)
                loopend_match = re.search(r"云云。",line)

                # print(f'loop match:{loop_match}')
                if loop_match and loop_match.start()==0:
                    var = self.c2e_dict[loop_match.group(1)]
                    python_code += f'{" "*in_loop*4}for i in range({var}):\n'
                    in_loop += 1
                    # print(in_loop)
                    line = line[loop_match.end():]
                    # continue
                
                # print(f'num match:{num_match}')
                elif num_match and num_match.start()==0:
                    num = cn2num(num_match.group(1))
                    var_chinese = num_match.group(2)
                    var_english = self.c2e(var_chinese)
                    # print(num,var)
                    python_code += f'{" "*in_loop*4}{var_english}={num} #{var_chinese}={num}\n'
                    # print(f'code:{python_code}')
                    line = line[num_match.end():]
                    # continue

                
                # print(f'string match:{string_match}')
                elif string_match and string_match.start()==0:
                    string = string_match.group(1)
                    # print(string)
                    # print(in_loop)
                    python_code += f'{" "*in_loop*4}print("{string}")\n'
                    line = line[string_match.end():]
                    # continue

                
                elif loopend_match and loopend_match.start()==0:
                    in_loop -= 1
                    line = line[loopend_match.end():]
                    # continue

                else:
                    raise SyntaxError(f'Syntax error in the beginning of code: {line}')

                # break

        return python_code

wenyan_code = '''吾有一数，曰「三」。名之曰「甲」。
为是「甲」遍。为是「甲」遍。吾有一言。曰「「问天地好在。」」。书之。云云。云云。'''
wenyan_object = wenyan(wenyan_code)
python_code = wenyan_object.wenyan2python()
print(python_code)
