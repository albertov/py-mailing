Ext.define('WebMailing.controller.Mailings', {
    extend: 'Ext.app.Controller',
    views: ['mailing.Panel'],
    refs: [
        {
            ref: 'grid',
            selector: 'mailing_grid'
        }, {
            ref: 'detail',
            selector: 'mailing_detail'
        }
    ],

    init: function() {
        this.control({
            "mailing_grid": {
                'select': this.onRowSelect,
                'afterrender': this.reloadStore
            }
        });
    },

    onRowSelect: function(_, record) {
        this.setActiveRecord(record);
    },

    reloadStore: function() {
        this.application.getStore('Mailings').load();
    },

    setActiveRecord: function(record) {
        if (this.record===record)
            return;
        this.record = record;
        this.getGrid().getSelectionModel().select(this.record);
        var c = this.application.getFreshController('Items');
        c.init(this.record, this.getDetail());
    }
});

