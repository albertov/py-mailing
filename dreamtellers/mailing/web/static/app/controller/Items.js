Ext.define('WebMailing.controller.Items', {
    extend: 'Ext.app.Controller',
    views: ['item.Tree'],
    refs: [
        {
            ref: 'tree',
            selector: 'item_tree'
        }, {
            ref: 'form',
            selector: 'item_form'
        }
    ],
    controllers: ['Categories'],
    init: function() {
        this.control({
            item_tree: {
                select: this.onEditNode,
                itemremove: Ext.bind(this.setActiveRecord, this, [null]),
                new_item: this.onNewItem,
                delete_node: this.onDeleteNode,
                edit_node: this.onEditNode,
                itemmove: this.updateItemPositions
            },
            "item_form field": {
                blur: this.onItemFormChange
            }

        });
    },
    setActiveRecord: function(record) {
        if (record!==null) {
            this.getForm().loadRecord(record);
        } else {
            this.getForm().disable();
        }
    },
    onEditNode: function(tree, node) {
        if (node.isItem()) {
            var record = node.get('record');
            if (record) {
                this.setActiveRecord(record);
            }
        } else {
            this.setActiveRecord(null);
        }
    },
    onItemFormChange: function() {
        var form=this.getForm().getForm();
        if (form.isValid())
            form.updateRecord();
    },
    onNewItem: function(tree, node) {
        var parent = node.get('record'),
            category_id = parent?parent.get('id'):null;
            item = tree.store.items.add({
                id: null,
                title: 'Sin título',
                category_id: category_id,
                type: 'Article' //XXX Preguntar tipo en combo
            })[0];
            this.setActiveRecord(item);
    },
    onDeleteNode: function(tree, node) {
        var record = node.get('record');
        if(!record)
            return;
        Ext.Msg.confirm(
            "Aviso",
            Ext.String.format('Se borrara permanentemente "{0}". ¿Seguro?',
                              record.get('title')),
            Ext.bind(this._confirmDeleteHandler, this, [record], 0)
        );
    },
    _confirmDeleteHandler: function(record, btn) {
        if (btn=="yes") {
            record.store.remove(record);
        }
    },
    updateItemPositions: function() {
        var pos=0;
        this.getTree().getStore().getRootNode().cascadeBy(function(n) {
            if (n.isItem()) {
                n.get('record').set('position', pos++);
            }
        });
    }
});
