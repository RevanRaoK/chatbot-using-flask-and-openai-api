from . import db


class Result(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  time = db.Column(db.String(50))
  messagetype = db.Column(db.String(100))
  message = db.Column(db.Text)
  def __repr__(self):
    return f"<Result {self.id} - {self.message[:20]}>"
