import time
from datetime import datetime
from typing import List
import csv
import os

#新增任務

# task name


# complexity:O(n)
def write_task_to_csv(task_dict : dict, filename: str):
    fieldnames  = ['任務編號', '事項標題', '事項描述', '結束日期', '狀態']# O(1)
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()#表投
        for state, task in task_dict.items():# O(n)
            row = {'任務編號': state}
            row.update(task)
            if "狀態" not in row:
                row['狀態'] = '代辦'
            writer.writerow(row)
            
#complexity : O(n)
def read_task_from_csv(filename: str) -> dict:
    tasks = {}
    if os.path.exists(filename):
        with open(filename, 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row['任務編號']
                tasks[key] = {
                    '事項標題': row.get('事項標題', ''),
                    '事項描述': row.get('事項描述', ''),
                    '結束日期': row.get('結束日期', ''),
                    '狀態': row.get('狀態', '代辦')  # 若沒有狀態則預設為 "代辦"
                }
    return tasks

#最壞情況下約 O(N²)
def set_task(task_dict : dict, csv_filename : str):
    existing_tasks = read_task_from_csv(csv_filename)#O(n)
    task_dict.update(existing_tasks)# O(n)
    print("請輸入工作內容，若不再新增請直接按 Enter 鍵離開。")

    while True:
        name = input("請輸入事項標題:")
        if name == "":
            break
        desc = input("請輸入描述")
        overdae = input("請輸入結束日期 (格式 YYYY/MM/DD)：")
        new_key = f"工作任務{len(task_dict) + 1}"#插入字典O(1)
        print(new_key)
        task_dict[new_key] = {
            '事項標題': name,
            '事項描述': desc,
            '結束日期': overdae
        }
        print(f"任務 {new_key} 已新增！\n")
        
        write_task_to_csv(task_dict, csv_filename)#每次執行都要重寫csv 資料越多操時間越高
        query_task(task_dict)
        quit = input('要繼續輸入嗎y/n:')
        if quit .lower() != 'y':
            break
    return task_dict

    # O(n)
def query_task(task_dict: dict):
    header = f"{'任務編號':<12}{'事項標題':<12}{'事項描述':<12}{'結束日期':<12}{'狀態':<10}"
    print(header)
    print("--" * len(header))
    for state, value in task_dict.items():
        status = value.get("狀態", "代辦")# 預設代辦
        print(f"{state:<12}{value['事項標題']:<12}{value['事項描述']:<20}{value['結束日期']:<12}{status:<10}")
    print("--" * len(header))
    
    
    #每個while 都只執行一次 o(1)
def input_new_task_fields():
    print("請輸入新的內容，若不更改則直接按 Enter：")
    
    # 事項標題 (可以是任意字串，不做額外檢查)
    while True:
        new_title = input("新的事項標題：")
        # 若輸入空字串，也視為不更改，直接跳出
        break

    # 事項描述 (同上)
    while True:
        new_desc = input("新的事項描述：")
        break

    # 結束日期：若有輸入，檢查格式是否為 YYYY/MM/DD
    while True:
        new_overdate = input("新的結束日期 (格式 YYYY/MM/DD)：")
        if new_overdate == "":
            break
        try:
            datetime.strptime(new_overdate, "%Y/%m/%d")
            break
        except ValueError:
            print("日期格式不正確，請重新輸入。")

    # 狀態 (例如：代辦、進行中、已完成)
    while True:
        new_status = input("新的狀態：")
        break

    return new_title, new_desc, new_overdate, new_status
#O(n)
def edit_task(task_dict : dict, filename : str):
    query_task(task_dict)# O(n)
    task_id = input("請輸入需編輯的任務編號:")#O(1)
    if task_id not in task_dict:
        print('找不到該任務')
        return task_dict
        
    new_title, new_desc, new_overdate, new_status = input_new_task_fields() #O(1)
    
    if new_title:
        task_dict[task_id]['事項標題'] = new_title
    if new_desc:
        task_dict[task_id]['事項描述'] = new_desc
    if new_overdate:
        task_dict[task_id]['結束日期'] = new_overdate
    if new_status:
        task_dict[task_id]['狀態'] = new_status
        
    print(f"{'任務已更新!'}")
    
    write_task_to_csv(task_dict, filename)#O(n)只寫入一次
    return task_dict

if __name__ == "__main__":
    # 假設已有任務字典
    tasks = {}
    csv_filename = "tasks.csv"
    tasks = set_task(tasks, csv_filename)


# write_task_to_csv 與 read_task_from_csv：O(n)
# set_task：最壞情況約為 O(N²)（主要來自每次新增任務都重寫整個 CSV）
# query_task：O(n)
# input_new_task_fields：O(1)
# edit_task：O(n)