# import pymysql
# import io
# from PIL import Image
# import re
#
# mysql_conn = pymysql.Connection(
#             host='localhost',
#             port=3306,
#             user='root',
#             password='12345678',
#             database='test',
#             charset='utf8',
#         )
#
# # 创建光标对象
# cs = mysql_conn.cursor()
# sql_str = 'select img_content from xinhuawang_img where id=60;'
# cs.execute(sql_str)
# # print(cs.fetchall()[0])
# # print(cs.fetchone()[0])
#
# # fout = open('image.jpg','wb')
# # fout.write(cs.fetchone()[1])
# cs.close()
# mysql_conn.commit()
# mysql_conn.close()
# #
# # # response_byte = cs.fetchone()[1]
# # # byte_stream = io.BytesIO(response_byte)
# # # roiImg = Image.open(byte_stream)#Image打开二进制流Byte字节流数据
# # # imgByteArr = io.BytesIO() # 创建一个空的Bytes对象
# # # roiImg.save(imgByteArr, format='png') # PNG就是图片格式
# # # imgByteArr = imgByteArr.getvalue() #保存的二进制流
#
# # img = re.findall('b"(.*?)"', cs.fetchone()[0])[0]
# print(cs.fetchone()[0])
# with open("E:/2.jpg", "wb") as f:
#     # f.write(cs.fetchone()[0])
#     f.write(b'x89PNG\r\nx1a\nx00x00')
#
