# ♟️ python\_chess\_fairino\_robot\_arm

Code điều khiển **robot arm FAIRINO** để chơi cờ vua bằng Python SDK trên **Ubuntu**.

---

## 📚 Thư viện & Cài đặt

Chạy các lệnh sau để chuẩn bị môi trường:

```bash
sudo apt update && sudo apt upgrade -y
pip install python-chess
sudo apt install stockfish
```

Về **FAIRINO SDK**, bạn có thể xem cách tải và sử dụng tại:
👉 [FAIRINO Python SDK Documentation](https://fairino-doc-en.readthedocs.io/latest/)

---

## ⚙️ Cấu hình trước khi chạy

Bạn cần kiểm tra **IP của robot** và **đường dẫn Stockfish** trong code:

```python
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
robot = Robot.RPC('192.168.58.2')
```

### Các tham số có thể thay đổi:

```python
BOARD_CENTER = (-500, 0, 250)   # Tọa độ tâm bàn cờ (x, y, z)
BOARD_SIZE = 480                # Kích thước bàn cờ (mm)
SQUARE_SIZE = BOARD_SIZE / 8    # Kích thước mỗi ô (60mm)

robot.SetSpeed(20)              # Tốc độ robot
```

---

## 🤖 Chạy chương trình

Bạn cần chắc chắn có **Docker virtual machine** với **FAIRINO**, sau đó chạy:

```bash
python robot_with_ai.py
# hoặc
python3 robot_with_ai.py
```

---

## 📏 Chiều cao quân cờ (mm)

```python
PIECE_HEIGHTS = {
    chess.PAWN: 30,    # Tốt
    chess.KNIGHT: 40,  # Mã
    chess.BISHOP: 45,  # Tượng
    chess.ROOK: 35,    # Xe
    chess.QUEEN: 50,   # Hậu
    chess.KING: 55     # Vua
}
```

---

## 📝 Ghi chú

* Nếu không biết Stockfish cài ở đâu, chạy lệnh:

  ```bash
  which stockfish
  ```

  Ví dụ:

  * `/usr/games/stockfish` (dùng trong code mẫu)
  * `/usr/bin/stockfish`
