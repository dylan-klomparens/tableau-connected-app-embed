from datetime import datetime, timedelta
from uuid import uuid4

from flask import Flask, render_template, request
from jwt import encode

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
	token = None
	if request.form:
		try:
			token = encode(
				payload={
					"iss": request.form["client-id"],
					"exp": datetime.utcnow() + timedelta(minutes=5),
					"jti": str(uuid4()),
					"aud": "tableau",
					"sub": request.form["username"],
					"scp": ["tableau:views:embed"],
				},
				key=request.form["secret-value"],
				algorithm="HS256",
				headers={
					'kid': request.form["secret-id"],
					'iss': request.form["client-id"]
				}
			)
		except:
			pass
	return render_template('index.html', form_data=request.form, token=token)


if __name__ == "__main__":
	app.run()
