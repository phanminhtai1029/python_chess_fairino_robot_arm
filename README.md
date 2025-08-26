# python\_chess\_fairino\_robot\_arm

Code điều khiển **robot arm FAIRINO** để chơi cờ vua bằng Python SDK trên **Ubuntu** hoặc **Windows**.

---

## Thư viện & Cài đặt

### 1. Cập nhật hệ thống & cài đặt thư viện

**Ubuntu:**

```bash
sudo apt update && sudo apt upgrade -y
pip install python-chess
sudo apt install stockfish
```

**Windows (PowerShell / CMD):**

```powershell
pip install python-chess
choco install stockfish   # nếu có Chocolatey, run with admin
# hoặc tải thủ công từ: https://stockfishchess.org/download/
```

Với **FAIRINO SDK**, bạn có thể xem cách tải và sử dụng tại:
[FAIRINO Python SDK Documentation](https://fairino-doc-en.readthedocs.io/latest/)

---

## Cấu hình trước khi chạy

Bạn cần kiểm tra **IP của robot** và **đường dẫn Stockfish** trong code:

```python
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")  # Ubuntu
engine = chess.engine.SimpleEngine.popen_uci("C:/Program Files/Stockfish/stockfish.exe")  # Windows

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

## Chạy chương trình

**Ubuntu:**

```bash
python robot_with_ai.py
# hoặc
python3 robot_with_ai.py
```

**Windows:**

```powershell
python robot_with_ai.py
```

> Bạn cần chắc chắn đã cài **Docker virtual machine** (Ubuntu) hoặc môi trường chạy FAIRINO SDK (Windows).

---

## Chiều cao quân cờ (mm)

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

## Ghi chú

* Nếu không biết **Stockfish** cài ở đâu:

**Ubuntu:**

```bash
which stockfish
```

**Windows (PowerShell):**

```powershell
where stockfish
```

Ví dụ:

* `/usr/games/stockfish` (Ubuntu, như code mẫu)
* `/usr/bin/stockfish` (Ubuntu)
* `C:\Program Files\Stockfish\stockfish.exe` (Windows)
