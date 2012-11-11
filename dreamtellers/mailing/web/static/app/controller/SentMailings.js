Ext.define('WebMailing.controller.SentMailings', {
    extend: 'Ext.app.Controller',
    models: ['SentMailing'],
    views: ['sent_mailing.Panel'], 
    refs: [
        {
            ref: 'groupChooser',
            selector: 'sent_mailings group_chooser'
        }, {
            ref: 'selectedGroups',
            selector: 'sent_mailings group_chooser grid[itemId="selected"]'
        }, {
            ref: 'sentMailingsGrid',
            selector: "sent_mailings sent_mailing_grid" 
        }
    ],

    init: function() {
        this.control({
            "sent_mailings  sent_mailing_grid": {
                select: this.onSentMailingSelect,
                new_item: this.onNewSentMailing,
                render: this.clearSelected,
                deselect: this.clearSelected
            },
            'sent_mailings group_chooser grid[itemId="available"]': {
                itemdblclick: this.onGroupDblClick
            },
            'sent_mailings group_chooser grid[itemId="selected"]': {
                drop: this.onGroupDrop,
                delete_item: this.onGroupDelete
            }
        });
    },
    onNewSentMailing: function(grid) {
        console.debug('onNewSentMailing', arguments);
        var r = grid.store.add({})[0];
        grid.store.on('write', function() {
            grid.rowEditor.startEdit(r, 0);
        }, this, {single:true});
    },

    onSentMailingSelect: function(grid, record) {
        console.debug('onSentMailingSelect', arguments);
        this.getGroupChooser().enable();
        record.group_sent_mailings().load({
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
        var sm = this.getSentMailingsGrid().getSelectionModel(),
            store = sm.getSelection()[0].group_sent_mailings();
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
        var sm = this.getSentMailingsGrid().getSelectionModel(),
            store = sm.getSelection()[0].group_sent_mailings();
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
