

test-server-install:
	cd tests/test-server && npm install

test-server-run:
	./tests/test-server/node_modules/.bin/json-server \
		--port 9500 --watch \
		./tests/test-server/test-server.json
