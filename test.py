from bottle import route, run, template
@route('/test0')
def choose():
	return template('testtemp0.tpl')
	return

@route('/test1')
def test_template1():
	return template('testtemp1.tpl')

@route('/test2')
def test_template2():
	return template('testtemp2.tpl')

@route('/test3')
def test_template3():
	return template('testtemp3.tpl')
#debug=True
run(host='localhost', port=8080)