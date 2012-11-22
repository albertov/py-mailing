Ext.define('WebMailing.controller.MailingDeliveries', {
    extend: 'Ext.app.Controller',
    models: ['MailingDelivery'],
    views: ['mailing_delivery.Panel'], 
    refs: [
        {
            ref: 'groupChooser',
            selector: 'mailing_deliveries group_chooser'
        }, {
            ref: 'selectedGroups',
            selector: 'mailing_deliveries group_chooser grid[itemId="selected"]'
        }, {
            ref: 'mailingDeliveriesGrid',
            selector: "mailing_deliveries mailing_delivery_grid" 
        }
    ],

    init: function() {
        this.control({
            "mailing_deliveries  mailing_delivery_grid": {
                select: this.onMailingDeliverySelect,
                new_item: this.onNewMailingDelivery,
                render: this.clearSelected,
                deselect: this.clearSelected
            },
            'mailing_deliveries group_chooser grid[itemId="available"]': {
                itemdblclick: this.onGroupDblClick
            },
            'mailing_deliveries group_chooser grid[itemId="selected"]': {
                drop: this.onGroupDrop,
                delete_item: this.onGroupDelete
            }
        });
    },
    onNewMailingDelivery: function(grid) {
        console.debug('onNewMailingDelivery', arguments);
        var r = grid.store.add({})[0];
        grid.store.on('write', function() {
            grid.rowEditor.startEdit(r, 0);
        }, this, {single:true});
    },

    onMailingDeliverySelect: function(grid, record) {
        console.debug('onMailingDeliverySelect', arguments);
        this.getGroupChooser().enable();
        record.group_mailing_deliveries().load({
            scope: this,
            callback: function(records, op, success) {
                if (success) {
                    this.clearSelected();
                    var store = this.getSelectedGroups().getStore();
                    Ext.each(records, function(r) {
                        r.getGroup(function(g) {
                            store.add(g.copy());
                        });
                    });
                    this.getGroupChooser().enable();
                }
            }
        });
    },
    addGroupsToSelected: function(records) {
        var sm = this.getMailingDeliveriesGrid().getSelectionModel(),
            store = sm.getSelection()[0].group_mailing_deliveries();
        store.suspendAutoSync();
        Ext.each(records, function(record) {
            store.add({group_id: record.get('id')});
        });
        store.resumeAutoSync();
        store.sync();
    },
    onGroupDblClick: function(_, record) {
        var store = this.getSelectedGroups().getStore();
        if (!store.getById(record.getId())) {
            store.add(record.copy());
            this.addGroupsToSelected([record]);
        }
    },
    onGroupDrop: function(_, data) {
        this.addGroupsToSelected(data.records);
    },

    onGroupDelete: function(_, group) {
        var sm = this.getMailingDeliveriesGrid().getSelectionModel(),
            store = sm.getSelection()[0].group_mailing_deliveries();
        var assoc = store.findRecord("group_id", group.get('id'));
        store.remove(assoc);
        group.store.remove(group);
    },

    clearSelected: function() {
        this.getGroupChooser().disable();
        var store = this.getSelectedGroups().getStore();
        store.removeAll();
    }
});
