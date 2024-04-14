import sqlite3


def calc():
    d = f"🎎 от 1 до 20"
    y = "🏤 Квиз"
    e = '10-80'
    # print(len(d[5:]))
    print(y[:1])


def del_data():
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
            """ DROP TABLE IF EXISTS level"""
    )
    connection.commit()
    connection.close()


def open_list():
    a = [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
    print(*a)
    for i in range(len(a)):
        print(*a[i])


def read_data_test():
    records_3 = []
    # records_age = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
    #  37, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 50, 52, 55, 56, 59, 60, 62, 64, 69, 70, 72, 73, 74, 76, 77, 78, 79, 85,
    #  86, 87, 89, 92, 97, 98, 99, 100, 101, 102, 103, 106, 107, 115, 116, 118, 123, 126, 128, 133, 134, 140, 147, 148,
    #  150, 151, 152, 154, 156, 158, 166, 171, 188, 203, 207, 220, 226, 230, 231, 253, 259, 261, 269, 280, 285, 294, 299,
    #  307, 310, 312, 316, 317, 318, 323, 327, 331, 333, 334, 346, 348, 351, 353, 366, 370, 380, 386, 389, 393, 421, 428,
    #  429, 454, 455, 456, 460, 463, 479, 480, 481, 493, 494, 498, 506, 511, 512, 516, 524, 531, 537, 541, 542, 554, 560,
    #  566, 567, 582, 589, 593, 597, 599, 600, 601, 602, 603, 615, 616, 622, 623, 624, 625, 626, 630, 642, 643, 645, 651,
    #  652, 653, 665, 674, 682, 683, 688, 689, 695, 703, 705, 716, 734, 738, 744, 746, 749, 750, 751, 752]
    a = [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
    # middle_records_members = []
    records_members = []
    # record = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    min_mem, max_mem = 2, 10
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
            """SELECT OID FROM level WHERE min_count >= ? AND max_count <= ?""", (min_mem, max_mem))
    records_3 = cursor.fetchall()
    connection.close()
    for i in records_3:
        if i in a:
            records_members.append(i)
    print(records_members)

    # print(records_3)
    # for i in records_3:
    #     if i != None:
    #         full_list.append(*i)
    # print(full_list)



def read_data_age_test():
    age_num = 14
    connection = sqlite3.connect("data.sqlite3")
    cursor = connection.cursor()
    cursor.execute(
        """SELECT OID FROM level WHERE age >= ?""", ([age_num]))
    records_1 = cursor.fetchall()
    connection.close()
    print(records_1)


if __name__ == '__main__':
    calc()
    # del_data()
    # open_list()
    # read_data_test()
    # read_data_age_test()

