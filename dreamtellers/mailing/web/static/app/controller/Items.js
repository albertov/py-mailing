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
                new_category: this.onNewCategory,
                new_item: this.onNewItem,
                delete_node: this.onDeleteNode,
                edit_node: this.onEditNode
            },
            "item_form field": {
                blur: this.onItemFormChange
            }

        });
    },
    setActiveRecord: function(record) {
        if (record!==null) {
            this.getForm().loadRecord(record);
        }
    },
    onEditNode: function(tree, node) {
        var record = node.get('record');
        if (record) {
            this.setActiveRecord(record);
        }
    },
    onItemFormChange: function() {
        var form=this.getForm().getForm();
        if (form.isValid())
            form.updateRecord();
    },
    onNewCategory: function(tree, node) {
        var parent = node.get('record');
        if (!parent) {
            var store=Ext.getStore('Categories');
            parent=store.getRootNode();
        }
        var category = parent.appendChild({
            title: 'Sin título', //i18n
            category_id:parent?parent.get('id'):null
        });
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
});
