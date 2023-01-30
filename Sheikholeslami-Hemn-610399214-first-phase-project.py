import csv, shlex



def handle_errors(user_input):
    # print(user_input)
    ## create
    if len(user_input) >= 2 and user_input[0] == 'create' and user_input[1] == "table":
        return True
    ## insert
    if len(user_input) >= 4 and user_input[0] == 'insert' and user_input[1] == "into" and user_input[3] == "values":
        return True
    ## select
    Select = False
    From = False
    Where = False
    for i in user_input:
        if i == "select":
            Select = True
        if i == "from":
            From = True
        if i == "where":
            Where = True
    if Select and From and Where:
        return True
    print('Syntax error: Please enter the correct syntax.')
    return False
    


def handle_create(schema,table_name):
    with open(table_name , 'w' , newline='') as file:
        writer = csv.writer(file)
        writer.writerow(schema)



def handle_insert(values,table_name):
    with open(table_name , 'a' , newline='') as file:
        writer = csv.writer(file)
        writer.writerow(values)

def type_check(dic , types):
    ans= {}
    i = 0
    for element in dic:
        if types[i] == 'int' and type(dic[element]) != 'int':
            print('type input error: Please enter the correct type of num.')
        elif types[i] == 'float' and type(dic[element]) != 'float':
            print('type input error: Please enter the correct type of num.')
        else:
            return True



def give_type(dic , type):
    ans = {}
    i=0
    for element in dic : 
        # ans[element] = (int (dic[element]) if type [i] == 'int' else dic [element])
        if type [i] == 'int':
            ans[element] = int(dic[element])
        elif type[i] == 'float':
            ans[element] = float(dic[element])
        else:
            ans[element] = dic[element]
        # ans[element] = (float (dic[element]) if type [i] == 'float' else dic [element])
        i+=1
    return ans 


def handle_select(table_name , type):
    with open(table_name , 'r' ) as file:
        csv_file = csv.DictReader(file)
        data = []
        for i in list(csv_file):
            data.append(give_type(dict(i)  , type))
    return data



def handle_select_condition(type_dic,condition, data ):
    for x in range(len(str(condition))):
        if condition[x] =='>' or condition[x] == '<' or condition[x] == '=':
            column_name, tag, value = condition[:x], condition[x], (condition[x+1:])

    result = []
    value = int(value) if type_dic[column_name] == 'int' else value
    value = float(value) if type_dic[column_name] == 'float' else value 

    for row in data:
        if tag == ">":
            if (row[column_name]) > value:
                result.append(row)
        elif tag == "=":
            if (row[column_name]) == value:
                result.append(row)
        else:
            if (row[column_name]) < value:
                result.append(row)
    return result



def handle_select_cloumn_name(column_names, data):
    if column_names == ["*"]:
        return data
    result = []
    for row in data:
        result.append({k:v for k,v in row.items() if k in column_names})
    return result




def split(string):
    string = [i.replace('(', '').replace(')', '').replace(',', ' ') for i in string]
    string = shlex.split(''.join(string))
    return string



def main():

    n = int(input())
    while 0<n:
        while True:

            user_input = input().lower()
            columns = split(user_input.split(" ")[1])
            user_input = split(user_input)
            if handle_errors(user_input=user_input) == True:
                break
        n-=1


        if user_input[0] == 'create':
            file_name = str(user_input[2]+'.csv')
            handle_create(schema = user_input[3::2],table_name = file_name)  
            type = [ user_input[i+1]  for i in range (3,len(user_input) , 2)]
            type_d = {user_input[i]:user_input[i+1]  for i in range (3,len(user_input) , 2)}
        elif user_input[0] == 'insert':
            file_name = str(user_input[2]+'.csv')
            handle_insert(values = user_input[4:] , table_name = file_name )  
        elif user_input[0] == 'select':
            file_name = str(user_input[2+len(columns)]+'.csv')
            data = handle_select(file_name  , type)
            data = handle_select_condition(type_d,condition=user_input[4+len(columns)], data=data  )
            data = handle_select_cloumn_name(columns, data)
            print(data)

                        
                

main()