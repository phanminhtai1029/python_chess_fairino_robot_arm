import chess
import chess.engine
from fairino import Robot

def print_board_with_coords(board: chess.Board):
    board_str = str(board).split("\n")
    for i, row in enumerate(board_str):
        print(f"{8 - i} {row}")   # In số hàng (8 → 1)
    print("  a b c d e f g h")    # In chữ cột

def square_to_xyz(square: str):
    """Chuyển từ ô cờ (vd: 'e4') sang tọa độ thực (x,y,z)."""
    sq = chess.parse_square(square)            # chuyển e4 -> số
    file = chess.square_file(sq)               # cột (0=a ... 7=h)
    rank = chess.square_rank(sq)               # hàng (0=1 ... 7=8)

    # Tính offset so với tâm bàn cờ
    x = BOARD_CENTER[0] + (rank - 3.5) * SQUARE_SIZE
    y = BOARD_CENTER[1] - (file - 3.5) * SQUARE_SIZE
    z = BOARD_CENTER[2]
    return (x, y, z)

def move_to_coordinates(move_uci: str):
    """Chuyển nước đi UCI (vd: 'e7e5') thành (tọa độ start, end)."""
    start_square = move_uci[0:2]
    end_square   = move_uci[2:4]
    return square_to_xyz(start_square), square_to_xyz(end_square)

def execute_robot(Start, End, piece_height):
    """Thực hiện hành động gắp của robot"""
    start1 = [Start[0], Start[1], basic[2], 180.000, 0.000, 90.000]
    start2 = [Start[0], Start[1], Start[2] + piece_height, 180.000, 0.000, 90.000]
    start3 = [Start[0], Start[1], basic[2], 180.000, 0.000, 90.000]

    end1 = [End[0], End[1], basic[2], 180.000, 0.000, 90.000]
    end2 = [End[0], End[1], End[2] + piece_height, 180.000, 0.000, 90.000]
    end3 = [End[0], End[1], basic[2], 180.000, 0.000, 90.000]

    tool, user, vel, blendR = 0, 0, 100.0, 0.0

    print(f"Robot di chuyển từ {Start} đến {End} với chiều cao quân cờ {piece_height}mm")

    # rtn1 = robot.MoveL(desc_pos=basic, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn1}")
    rtn2 = robot.MoveL(desc_pos=start1, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn2}")
    rtn3 = robot.MoveL(desc_pos=start2, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn3}")
    rtn4 = robot.MoveL(desc_pos=start3, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn4}")
    rtn5 = robot.MoveL(desc_pos=end1, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn5}")
    rtn6 = robot.MoveL(desc_pos=end2, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn6}")
    rtn7 = robot.MoveL(desc_pos=end3, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn7}")
    # rtn8 = robot.MoveL(desc_pos=basic, tool=tool, user=user, vel=vel, blendR=blendR)
    # print(f"movel errcode: {rtn8}")

def get_piece_height(board: chess.Board, square_str: str):
    """Lấy chiều cao của quân cờ tại một ô"""
    square = chess.parse_square(square_str)
    piece = board.piece_at(square)
    if piece:
        return PIECE_HEIGHTS.get(piece.piece_type, 50)  # Mặc định 50 nếu không tìm thấy
    return 0  # Không có quân cờ

# Trỏ tới stockfish (apt cài)
engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

# Tạo bàn cờ mới
board = chess.Board()

BOARD_CENTER = (-500, 0, 250)   # (x, y, z)
BOARD_SIZE = 480                # mm
SQUARE_SIZE = BOARD_SIZE / 8    # 60mm

robot = Robot.RPC('192.168.58.2')
basic = [BOARD_CENTER[0], BOARD_CENTER[1], BOARD_CENTER[2]+150, 180.000, 0.000, 90.000]
robot.SetSpeed(20)

# Dictionary lưu chiều cao của từng loại quân cờ (mm)
PIECE_HEIGHTS = {
    chess.PAWN: 30,    # Tốt
    chess.KNIGHT: 40,  # Mã
    chess.BISHOP: 45,  # Tượng
    chess.ROOK: 35,    # Xe
    chess.QUEEN: 50,   # Hậu
    chess.KING: 55     # Vua
}

# Tọa độ khu vực để các quân cờ đã bị ăn (Graveyard)
# Ví dụ: đặt chúng thành một hàng ở bên cạnh bàn cờ
captured_pieces_coords = []
for i in range(16):  # Tối đa 15 quân cờ có thể bị ăn bởi một bên
    if i < 8:
        x = (BOARD_CENTER[0] + BOARD_SIZE / 2) - (i * (SQUARE_SIZE * 0.8))
        y = (BOARD_CENTER[1] + BOARD_SIZE / 2) + 50
        z = BOARD_CENTER[2]
    else:
        x = (BOARD_CENTER[0] + BOARD_SIZE / 2) - ((i - 8) * (SQUARE_SIZE * 0.8))
        y = (BOARD_CENTER[1] + BOARD_SIZE / 2) + 50 + SQUARE_SIZE
        z = BOARD_CENTER[2]

    captured_pieces_coords.append((x, y, z))

captured_pieces_count = 0

def remove_piece_from_board(square_to_clear_xyz, piece_height):
    """Điều khiển robot di chuyển một quân cờ từ vị trí trên bàn cờ đến vị trí tiếp theo trong "nghĩa địa"."""
    global captured_pieces_count
    if captured_pieces_count < len(captured_pieces_coords):
        graveyard_pos = captured_pieces_coords[captured_pieces_count]
        print(f"Di chuyển quân cờ bị ăn từ {square_to_clear_xyz} đến khu vực chờ {graveyard_pos}")
        execute_robot(square_to_clear_xyz, graveyard_pos, piece_height)
        captured_pieces_count += 1
    else:
        print("Khu vực chứa quân cờ đã đầy!")

promotion_pieces_coords_black = {
    chess.QUEEN: (BOARD_CENTER[0] + BOARD_SIZE/2, BOARD_CENTER[1] - BOARD_SIZE/2 - 100, BOARD_CENTER[2]),
    chess.ROOK: (BOARD_CENTER[0] + BOARD_SIZE/2 - 90, BOARD_CENTER[1] - BOARD_SIZE/2 - 100, BOARD_CENTER[2]),
    chess.BISHOP: (BOARD_CENTER[0] + BOARD_SIZE/2 - 150, BOARD_CENTER[1] - BOARD_SIZE/2 - 100, BOARD_CENTER[2]),
    chess.KNIGHT: (BOARD_CENTER[0] + BOARD_SIZE/2 - 210, BOARD_CENTER[1] - BOARD_SIZE/2 - 100, BOARD_CENTER[2])
}


# ===== THÊM MỚI: Hàm xử lý phong cấp CHO AI (ĐEN) =====
def handle_ai_promotion(move: chess.Move, board: chess.Board):
    """Xử lý phong cấp cho robot AI (đen)"""
    move_uci = move.uci()

    # Xác định loại quân được phong
    promoted_piece_type = move.promotion if move.promotion else chess.QUEEN

    # Lấy vị trí của con tốt và vị trí đích
    pawn_start_xyz, pawn_end_xyz = move_to_coordinates(move_uci[0:4])
    pawn_height = PIECE_HEIGHTS[chess.PAWN]

    print(f"AI thực hiện Phong cấp tốt thành {chess.piece_name(promoted_piece_type).capitalize()}...")

    # Kiểm tra nếu có ăn quân khi phong cấp
    if board.is_capture(move):
        end_square_name = move_uci[2:4]
        captured_piece_height = get_piece_height(board, end_square_name)
        captured_piece_xyz = square_to_xyz(end_square_name)

        # Robot dọn quân cờ bị ăn
        print("Dọn quân cờ bị ăn trước khi phong cấp...")
        remove_piece_from_board(captured_piece_xyz, captured_piece_height)

    # Bước 1: Di chuyển con tốt đến vị trí phong cấp
    print("Di chuyển tốt đến hàng cuối...")
    execute_robot(pawn_start_xyz, pawn_end_xyz, pawn_height)

    # Bước 2: Bỏ con tốt vào "nghĩa địa" luôn
    print("Đưa tốt đã phong cấp vào khu vực quân bị loại...")
    remove_piece_from_board(pawn_end_xyz, pawn_height)

    # Bước 3: Lấy quân mới từ khu vực phong cấp
    new_piece_position = promotion_pieces_coords_black[promoted_piece_type]
    new_piece_height = PIECE_HEIGHTS[promoted_piece_type]

    print(f"Lấy quân {chess.piece_name(promoted_piece_type).capitalize()} từ khu vực phong cấp...")
    execute_robot(new_piece_position, pawn_end_xyz, new_piece_height)

    print(f"Phong cấp hoàn tất!")

while not board.is_game_over():
    # In bàn cờ hiện tại
    print_board_with_coords(board)
    print("\nNước đi hợp lệ của bạn (ví dụ: e2e4, e7e8q cho phong hậu, quit, exit, stop):")

    # Người nhập nước đi
    move_input = input(">>> ")

    if move_input.lower() in ["quit", "exit", "stop"]:
        print("Bạn đã dừng ván cờ.")
        break

    try:
        move = chess.Move.from_uci(move_input)
        if move in board.legal_moves:
            board.push(move)  # Trắng đi
        else:
            print("Nước đi không hợp lệ, thử lại!")
            continue
    except:
        print("Sai cú pháp! (dùng dạng e2e4, hoặc e7e8q cho phong hậu)")
        continue

    # Kiểm tra sau khi bạn đi
    if board.is_game_over():
        break

    # AI (đen) đi
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    engine.configure({"Skill Level": 1})  # 1-5 là rất yếu, phù hợp test

    # Giảm thời gian suy nghĩ
    result = engine.play(board, chess.engine.Limit(time=0.1, depth=3))

    # result = engine.play(board, chess.engine.Limit(time=1))  # AI nghĩ 1 giây
    ai_move = result.move
    print("\nAI đi:", ai_move, "\n")

    move_uci = ai_move.uci()

    # 0. Kiểm tra Phong cấp CHO AI
    if ai_move.promotion:
        handle_ai_promotion(ai_move, board)

    # 1. Xử lý Nhập thành (Castling)
    elif board.is_castling(ai_move):
        print("AI thực hiện Nhập thành...")
        # Di chuyển Vua
        king_start_xyz, king_end_xyz = move_to_coordinates(move_uci)
        king_height = PIECE_HEIGHTS[chess.KING]
        execute_robot(king_start_xyz, king_end_xyz, king_height)

        # Xác định và di chuyển Xe
        rook_move_uci = ""
        if move_uci == "e8g8":
            rook_move_uci = "h8f8"  # Đen nhập thành cánh vua
        elif move_uci == "e8c8":
            rook_move_uci = "a8d8"  # Đen nhập thành cánh hậu
        # (Bạn có thể thêm logic cho Trắng nếu AI chơi Trắng)
        # elif move_uci == "e1g1": rook_move_uci = "h1f1"
        # elif move_uci == "e1c1": rook_move_uci = "a1d1"

        if rook_move_uci:
            rook_start_xyz, rook_end_xyz = move_to_coordinates(rook_move_uci)
            rook_height = PIECE_HEIGHTS[chess.ROOK]
            execute_robot(rook_start_xyz, rook_end_xyz, rook_height)

    # 2. Xử lý Bắt Tốt qua đường (En Passant)
    elif board.is_en_passant(ai_move):
        print("AI thực hiện Bắt Tốt qua đường...")
        # Tọa độ con tốt của AI
        pawn_start_xyz, pawn_end_xyz = move_to_coordinates(move_uci)
        pawn_height = PIECE_HEIGHTS[chess.PAWN]

        # Xác định vị trí con tốt bị bắt
        # Vị trí này có cùng cột với ô đến và cùng hàng với ô xuất phát của con tốt AI
        to_square = ai_move.to_square
        from_square = ai_move.from_square
        captured_pawn_square = chess.square(chess.square_file(to_square), chess.square_rank(from_square))
        captured_pawn_square_name = chess.square_name(captured_pawn_square)
        captured_pawn_xyz = square_to_xyz(captured_pawn_square_name)

        # Robot dọn con tốt bị bắt
        remove_piece_from_board(captured_pawn_xyz, pawn_height)
        # Robot di chuyển con tốt của AI
        execute_robot(pawn_start_xyz, pawn_end_xyz, pawn_height)

    # 3. Xử lý Ăn quân thông thường
    elif board.is_capture(ai_move):
        print("AI thực hiện Ăn quân...")
        # Vị trí quân cờ bị ăn là ở ô đích
        end_square_name = move_uci[2:4]
        captured_piece_height = get_piece_height(board, end_square_name)
        captured_piece_xyz = square_to_xyz(end_square_name)

        # Robot dọn quân cờ bị ăn
        remove_piece_from_board(captured_piece_xyz, captured_piece_height)

        # Lấy chiều cao của quân cờ đang di chuyển
        start_square_name = move_uci[0:2]
        moving_piece_height = get_piece_height(board, start_square_name)

        # Robot di chuyển quân cờ của AI
        start_xyz, end_xyz = move_to_coordinates(move_uci)
        execute_robot(start_xyz, end_xyz, moving_piece_height)

    # 4. Nước đi bình thường
    else:
        print("AI thực hiện nước đi thường...")
        start_square_name = move_uci[0:2]
        piece_height = get_piece_height(board, start_square_name)

        start, end = move_to_coordinates(move_uci)
        execute_robot(start, end, piece_height)

    tool, user, vel, blendR = 0, 0, 100.0, 0.0
    robot.MoveL(desc_pos=basic, tool=tool, user=user, vel=vel, blendR=blendR)

    board.push(result.move)

# Kết thúc ván cờ
print(board)
print("\nVán cờ kết thúc:", board.result())

robot.CloseRPC()
engine.quit()