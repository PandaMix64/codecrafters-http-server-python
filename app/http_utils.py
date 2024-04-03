class HttpRequest:
    method = ""
    path = ""
    protocol = ""
    headers = {}
    msg_body = ""

    def __init__(self, request_data: str) -> None:
        # rq_segments = request_data.split("\n")
        rq_segments = []
        for request_segment in request_data.split("\n"):
            valid_segment = request_segment.replace("\r", "")
            if len(valid_segment.strip()) == 0:
                continue
            rq_segments.append(valid_segment)
        i = 0
        for segment in rq_segments:
            if i == 0:
                segment_parts = segment.split()
                s_count = len(segment_parts) 
                if s_count >= 1:
                    self.method = segment_parts[0]
                if s_count >= 2:
                    self.path = segment_parts[1]
                if s_count >= 3:
                    self.protocol = segment_parts [2]
                i = i + 1
                continue
            header, header_data = segment.split(":", 1)
            self.headers[header.strip().lower()] = header_data.strip()
            i = i + 1