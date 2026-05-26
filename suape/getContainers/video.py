import os
import time
from pathlib import Path

import cv2


def initialize_tracker() -> cv2.Tracker:
    return cv2.TrackerCSRT_create()


def save_cropped_image(frame, bbox: tuple, save_dir: Path) -> None:
    x, y, w, h = (int(v) for v in bbox)
    cropped = frame[y : y + h, x : x + w]

    save_dir.mkdir(parents=True, exist_ok=True)
    filename = save_dir / f"container_{time.strftime('%Y%m%d-%H%M%S')}.png"
    cv2.imwrite(str(filename), cropped)
    print(f"Imagem salva: {filename}")


def track_container_in_video(video_path: str, save_dir: Path) -> None:
    while True:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Erro: não foi possível abrir o vídeo '{video_path}'.")
            return

        ret, frame = cap.read()
        if not ret:
            print("Erro: não foi possível ler o primeiro frame.")
            cap.release()
            return

        print("Selecione a área do container no primeiro frame e pressione ENTER ou ESPAÇO.")
        bbox = cv2.selectROI("Selecione o Container", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Selecione o Container")

        tracker = initialize_tracker()
        tracker.init(frame, bbox)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fim do vídeo. Reiniciando...")
                cap.release()
                break

            success, bbox = tracker.update(frame)

            if success:
                x, y, w, h = (int(v) for v in bbox)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 16)
                cv2.putText(frame, f"X: {x}, Y: {y}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
                if x < 700:
                    cv2.putText(frame, "Desembarque 1", (999, 700), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 8)
                save_cropped_image(frame, bbox, save_dir)
            else:
                cv2.putText(frame, "Falha no rastreamento", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            cv2.imshow("Rastreamento de Container", frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                return


if __name__ == "__main__":
    VIDEO_PATH = "./getContainers/video/video_fast_4.mov"
    SAVE_DIR = Path("./images/images")
    track_container_in_video(VIDEO_PATH, SAVE_DIR)
