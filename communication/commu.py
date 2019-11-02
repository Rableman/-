import socket

class communication():
	def __init__(self, mode, ip, port):
		self.mode = mode
		self.ip = ip
		self.port = port

	def server(self, senddata="", clientnum=1):
		# AF = IPv4 という意味
		# TCP/IP の場合は、SOCK_STREAM を使う
		data = {"ip":"", "data":""}
		if self.mode == "tcp":
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				# IPアドレスとポートを指定
				s.bind((self.ip, self.port))
				# 1 接続
				s.listen(clientnum)
				# connection するまで待つ
				while not data["ip"]:
					# 誰かがアクセスしてきたら、コネクションとアドレスを入れる
					conn, addr = s.accept()
					with conn:
						while True:
							# データを受け取る
							msg = conn.recv(1024)
							if not msg:
								break
							data["ip"] = addr[0]
							data["data"] += msg.decode(encoding="UTF-8")
							# クライアントにデータを返す(b -> byte でないといけない)
							conn.sendall(senddata.encode(encoding="UTF-8"))
			s.close()
		elif self.mode == "udp" or self.mode == "broadcast":
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			# バインドしておく
			s.bind((self.ip, self.port))
			while not data["ip"]:
				while True:
					# 受信
					msg, address = s.recvfrom(1024)
					if not msg:
						break
					data["ip"] = address
					data["data"] += msg.decode(encoding="UTF-8")
			s.close()
		return data

	def client(self, senddata):
		data = {"ip":self.ip, "data":""}
		if self.mode == "tcp":
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				# サーバを指定
				s.connect((self.ip, self.port))
				# サーバにメッセージを送る
				s.sendall(senddata.encode(encoding="UTF-8"))
				# ネットワークのバッファサイズは1024。サーバからの文字列を取得する
				data["data"] += s.recv(1024).decode(encoding="UTF-8")
				#
			s.close()
		elif self.mode == "udp" or self.mode == "broadcast":
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			if self.mode == "broadcast":
				s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			s.sendto(senddata.encode(encoding="UTF-8"), (self.ip, self.port))
			s.close()
		return data
