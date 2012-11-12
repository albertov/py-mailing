Ext.define('WebMailing.store.ItemTreeStore', {
    extend: 'Ext.data.TreeStore',
    requires: [
        'WebMailing.model.ItemNode'
    ],
    model: 'WebMailing.model.ItemNode',

    constructor: function(config) {
        this.callParent(arguments);
        this.items = this.mailing.items();
        this.setRootNode({
            expanded: true,
            title: this.mailing.getTitle()
        });
        this.items.on('refresh', this.updateTree, this);
        this.categories.on('refresh', this.updateTree, this);
        this.updateTree();
    },
    destroy: function() {
        this.items.un('refresh', this.updateTree, this);
        this.categories.un('refresh', this.updateTree, this);
    },

    load: function(me, records) {
        if (!(this.categories.getRootNode() &&
              this.categories.getRootNode().hasChildNodes())) {
            this.categories.load();
        }
        if (this.items.getCount()<1) {
            this.items.load();
        }
    },
    updateTree: function() {
        this.suspendEvents(true);
        this.getRootNode().removeAll();
        this._updateCategories();
        this._updateItems();
        this.resumeEvents();
    },
    _updateCategories: function() {
        function copy_node(src, dst) {
            if (!(src && dst)) return;
            // Copy childs recursively
            src.eachChild(function(sNode) {
                var dNodeId = 'category-'+sNode.get('id'),
                    data = Ext.applyIf({
                        id:dNodeId,
                        expanded: true,
                        record: sNode,
                        children: []
                    }, sNode.data);
                dNode = new WebMailing.model.ItemNode(data);
                dst.appendChild(dNode);
                copy_node(sNode, dNode);
            });
        }
        copy_node(this.categories.getRootNode(), this.getRootNode());
    },
    _updateItems: function() {
        // Copy items
        var root = this.getRootNode();
        this.items.each(function(item) {
            var itemId = 'item-'+(item.phantom?Ext.id():item.get('id'));
            var data = Ext.applyIf({
                id: itemId,
                leaf:true,
                record: item
            }, item.data);
            var newItem = new WebMailing.model.ItemNode(data),
                catId = item.get('category_id'), cat;
            if (catId) {
                cat = root.findChild('id', 'category-'+catId, true);
            } else {
                cat = root;
            }
            cat = cat?cat:root;
            var pos = newItem.get('position');
            var c = cat;
            while (c.parentNode) {
                c.set('position', pos);
                c = c.parentNode;
            }
            cat.appendChild(newItem);
            cat.sort(function(a,b) {
                return a.get('position')-b.get('position');
            }, true);
        }, this);
        root.sort(function(a,b) {
            return a.get('position')-b.get('position');
        }, true);
    }
});
