

test-server-install:
	cd ./test-server && npm install

test-server-run:
	./test-server/node_modules/.bin/json-server \
		--port 9500 --watch \
		./test-server/test-server.json
