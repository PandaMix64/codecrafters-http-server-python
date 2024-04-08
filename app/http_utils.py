class HttpRequest:
    method = ""
    path = ""
    protocol = ""
    headers = {}
    body = ""

    def __init__(self, request_data: str) -> None:
        # rq_segments = request_data.split("\n")
        rq_segments:list[str] = []
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
                    self.protocol = segment_parts[2]
                i = i + 1
                if self.method == "POST":
                    i = i + 1
                continue
            if i == len(rq_segments):
                self.body = segment
                continue
            header, header_data = segment.split(":", 1)
            self.headers[header.strip()] = header_data.strip()
            i = i + 1

    def __str__(self) -> str:
        headers = ""
        for header, value in self.headers.items():
            if headers == "":
                headers += f"{header}: {value}"
            headers += f"\r\n{header}: {value}"
        return f"{self.method} {self.path} {self.protocol}\r\n{headers}\r\n\r\n{self.body}"

class HttpResponse:
    response = ""
    request:HttpRequest
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def process_get(self, content:str, content_type:str = "text/plain", status:int = 200, msg:str = "OK"):
        self.response = f"{self.request.protocol} {status} {msg}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        return self.response

    def process_post(self, content = {}, content_type:str = "application/json",status:int = 201, msg:str = "Created", headers:dict={}):
        extra_h = ""
        for header, value in headers.items():
            if extra_h == "":
                extra_h += f"{header}: {value}"
                continue
            extra_h += f"\r\n{header}: {value}"
        self.response = f"{self.request.protocol} {status} {msg}\r\nContent-Type: {content_type}\r\n{extra_h}\r\n\r\n{content}"
        return self.response
    
    def not_found(self):
        return "HTTP/1.1 404 Not Found\r\nConnection: close\r\nContent-Length: 0\r\n\r\n"

    def __str__(self) -> str:
        if self.response == "":
            if self.request.method == "POST":
                return self.process_post("")
            else:
                return self.process_get("", status=404, msg = "Not Found")
        return self.response