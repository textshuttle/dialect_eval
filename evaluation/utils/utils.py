

def load_segments(path_to_file):
    with open(path_to_file, encoding='utf-8') as f:
        segments = [line.strip() for line in f.readlines()]
    return segments

def write_segments(path_to_file, segments):
    with open(path_to_file, "w") as f:
        for segment in segments:
            f.write(f"{segment}\n")