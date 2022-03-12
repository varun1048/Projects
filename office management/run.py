from application import app

if __name__ == "__main__":
    ip = "192.168.1.2"
    print(f"\t {ip}") 
    # app.run(debug = True)
    
    # ip = "192.168.1.2"
    app.run(host=ip, port=5000, debug=True, threaded=False)