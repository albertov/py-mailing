import datetime
from . import BaseViewTest


class TestMailingDeliveryViews(BaseViewTest):
    def test_create_a_good_one(self):
        m = self._makeMailing(number=0)
        d = datetime.datetime(2008,1,1)
        self.session.add(m)
        self.session.flush()
        data = dict(mailing_id=m.id, programmed_date=d.isoformat())
        resp = self.app.post_json('/mailing_delivery/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['mailing_deliveries']), 1)
        item = resp.json['mailing_deliveries'][0]
        for k in data:
            self.assertEqual(item[k], data[k])

    def test_associate_group(self):
        sm = self._makeMailingDelivery(
            mailing = self._makeMailing(number=0),
            programmed_date = datetime.datetime(2008,1,1)
            )
        g = self._makeGroup(name='foo')
        self.session.add(sm)
        self.session.add(g)
        self.session.flush()

        data = dict(mailing_delivery_id=sm.id, group_id=g.id)
        resp = self.app.post_json('/group_mailing_delivery/', data)
        self.assertTrue(resp.json['success'])
        self.assertEqual(len(resp.json['group_mailing_deliveries']), 1)
        item = resp.json['group_mailing_deliveries'][0]
        for k in data:
            self.assertEqual(item[k], data[k])
        self.failUnlessEqual(1, len(sm.query.one().groups))

    def test_delete_association(self):
        sm = self._makeMailingDelivery(
            mailing = self._makeMailing(number=0),
            programmed_date = datetime.datetime(2008,1,1)
            )
        g = self._makeGroup(name='foo')
        self.session.add(sm)
        self.session.add(g)
        self.session.flush()

        data = dict(mailing_delivery_id=sm.id, group_id=g.id)
        resp = self.app.post_json('/group_mailing_delivery/', data)
        self.assertTrue(resp.json['success'])
        item = resp.json['group_mailing_deliveries'][0]
        self.failUnlessEqual(1, len(sm.query.one().groups))
        resp = self.app.delete('/group_mailing_delivery/%s'%str(item['id']))
        self.assertTrue(resp.json['success'])
        self.failUnlessEqual(0, len(sm.query.one().groups))
