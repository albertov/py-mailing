Ext.define('WebMailing.controller.Mailings', {
    extend: 'Ext.app.Controller',
    views: ['mailing.Panel'],
    refs: [
        {
            ref: 'panel',
            selector: 'mailings'
        }, {
            ref: 'grid',
            selector: 'mailing_grid'
        }, {
            ref: 'form',
            selector: 'mailing_form'
        }, {
            ref: 'detail',
            selector: 'mailing_detail'
        }
    ],

    init: function() {
        this.control({
            "mailing_grid": {
                'select': this.onRowSelect,
                'save_mailings': this.syncMailings,
                'deselect': this.onRowDeSelect,
                'afterrender': this.reloadStore,
                'new_mailing': this.onNewMailing,
                'delete_mailing': this.onDeleteMailing
            },
            "mailing_form field": {
                "blur": this.onMailingFormDirtyChange
            }
        });
        this.mailings = Ext.getStore('Mailings');
        this.mon(this.mailings, 'beforeload', this._saveSelection, this);
        this.mon(this.mailings, 'load', this._restoreSelection, this);
        this.mon(this.mailings, 'write', this.refreshView, this);
        this.mon(Ext.getStore('Categories'), 'write', this.refreshView, this);
    },

    _saveSelection: function() {
        var grid=this.getGrid(),
            sm=grid.getSelectionModel(),
            selection=sm.getSelection();
        var ids = []
        for (var i=0; i<selection.length; i++) {
            var id = selection[i].getId();
            ids.push(id);
        }
        sm._oldSelection = ids;
    },
    _restoreSelection: function() {
        var grid=this.getGrid(),
            sm=grid.getSelectionModel();
         if (sm._oldSelection) {
             var store = grid.getStore(), selection=[];
             Ext.each(sm._oldSelection, function(id) {
                 var n = store.getById(id);
                 if (n!==null) 
                     selection.push(n);
             });
             delete sm._oldSelection;
             if (selection.length)
                 sm.select(selection);
         }
    },

    onRowSelect: function(grid, record) {
        this.setActiveRecord(record);
    },

    onRowDeSelect: function() {
        this.setActiveRecord(null);
    },

    reloadStore: function() {
        this.mailings.reload();
    },

    refreshView: function() {
        this.getDetail().refresh();
    },

    setActiveRecord: function(record) {
        if (record) {
            this.getGrid().getSelectionModel().select(record);
            this.getDetail().setRecord(record);
            this.getDetail().enable();
        } else {
            this.getGrid().getSelectionModel().deselectAll();
            this.getDetail().disable();
        }
    },

    onDeleteMailing: function(grid, record) {
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.getTitle()),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            var s = record.store;
            this.setActiveRecord(null);
            s.remove(record);
            this.syncMailings();
        }
    },
    onNewMailing: function(grid) {
        var store = this.application.getStore('Mailings'),
            rec = store.add({date: new Date})[0];
        this.setActiveRecord(null);
        this.syncMailings({
            success: Ext.bind(this.setActiveRecord, this, [rec])
        });
    },
    syncMailings: function(config) {
        var store = this.application.getStore('Mailings');
        var mask = this.getPanel().loadMask;
        mask.show();
        store.sync({
            failure: function() {
                mask.hide();
            },
            success: function() {
                var syncing=0;
                function maybeHide(decrement) {
                    if (decrement) syncing--;
                    if (syncing==0) {
                        mask.hide();
                    }
                }
                store.each(function(r) {
                    var s = r.items();
                    if (s.getModifiedRecords().length>0 ||
                        s.getRemovedRecords().length>0) {
                        syncing++;
                        s.sync({
                            success: function() {
                                maybeHide(true);
                                if (config.success) {
                                    config.success();
                                }
                            },
                            failure: function() {
                                maybeHide(true);
                                if (config.failure) {
                                    config.failure();
                                }
                            }
                        });
                    }
                });
                maybeHide(false);
            }
        });
    },
    onMailingFormDirtyChange: function(field) {
        var form = this.getForm().getForm();
        if (form.isValid()) {
            form.updateRecord();
        }
    }
});
