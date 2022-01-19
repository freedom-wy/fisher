from app import create_app
from app.models.drift import Drift
from app.libs.enums import PendingStatus
from app.models.user import User

app = create_app()


@app.route("/test/<gid>")
def test_sql(gid):
    data = Drift.query.filter(Drift.gift_id == gid, Drift._pending == PendingStatus.Waiting.value).first()
    return data.book_title


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
