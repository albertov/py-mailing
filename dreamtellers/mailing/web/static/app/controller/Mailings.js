Ext.define('WebMailing.controller.Mailings', {
    extend: 'Ext.app.Controller',
    views: ['mailing.Panel'],
    stores: ['Mailings', 'Categories', 'Templates'],
    models: ['Mailing'],
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
            ref: 'itemForm',
            selector: 'mailing_detail item_form'
        }, {
            ref: 'detail',
            selector: 'mailing_detail'
        }
    ],

    init: function() {
        this.control({
            "mailing_grid": {
                'select': this.onRowSelect,
                'beforedeselect': this.checkIfSaveIsNeeded,
                'deselect': this.onRowDeSelect,
                'afterrender': this.reloadStore,
                'new_item': this.onNewMailing,
                'delete_item': this.onDeleteMailing
            },
            "mailing_form field": {
                "blur": this.onMailingFormDirtyChange
            },
            "item_tree": {
                beforedeselect: this.checkIfSaveIsNeeded,
            },
            "mailing_view combo": {
                select: this.onTemplateComboSelect,
            }
        });
        this.mailings = Ext.getStore('Mailings');
        this.mon(this.mailings, 'beforeload', this._saveSelection, this);
        this.mon(this.mailings, 'load', this._restoreSelection, this);
        this.mon(this.mailings, 'write', this.refreshView, this);
        this.mon(Ext.getStore('Categories'), 'write', this.refreshView, this);
        this.mon(Ext.getStore('Templates'), 'write', this.refreshView, this);
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

    checkIfSaveIsNeeded: function() {
        var f = this.getItemForm().getForm();
        if (f.getRecord() && f.isDirty()) {
            Ext.MessageBox.show({
                title: "Aviso", // i18n
                msg: "El item contiene cambios sin guardar. ¿Desea guardarlos?",
                icon: Ext.MessageBox.WARNING,
                buttons: Ext.Msg.YESNOCANCEL,
                fn: function(btn) {
                    if (btn=="yes") {
                        f.updateRecord();
                    } else if (btn=="no") {
                        f.reset();
                    }
                }
            });
            return false;
        } else {
            return true;
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
        if (!this.checkIfSaveIsNeeded())
            return;
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
        }
    },
    onNewMailing: function(grid) {
        if (!this.checkIfSaveIsNeeded())
            return;
        var store = this.application.getStore('Mailings'),
            rec = store.add({date: new Date})[0];
        store.on('write', Ext.bind(this.setActiveRecord, this, [rec]),
                 this, {single:true})
    },
    onTemplateComboSelect: function(combo, records) {
        var record = this.getDetail().getRecord();
        if (record) {
            record.addTemplate(records[0]);
        }
    }
});
