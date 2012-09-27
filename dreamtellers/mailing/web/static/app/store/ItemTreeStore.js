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
        this.mon(this.items, 'datachanged', this.onItemsChange, this);
        this.mon(this.categories, 'append', this.onCategoriesLoad, this);
        this.mon(this.categories, 'update', this.onCategoriesLoad, this);
        this.mon(this.categories, 'remove', this.onCategoriesLoad, this);
        this.relayEvents(this.items, ['write']);
        this.relayEvents(this.categories, ['write']);
        this._updateCategories();
        this._updateItems();

    },

    sync: function() {
        this.categories.sync();
        this.items.sync();
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
    onItemsChange: function() {
        this._updateItems();
    },
    onCategoriesLoad: function() {
        this._updateCategories();
        this._updateItems();
    },
    _updateCategories: function() {
        function copy_node(src, dst) {
            if (!(src && dst)) return;
            // prune children from dst that are not in src
            dst.eachChild(function(dNode) {
                if (!dNode) return;
                var dNodeId = dNode.get('id');
                if (dNodeId && dNodeId.indexOf('category-')>-1) {
                    var sNodeId = parseInt(dNodeId.slice(dNodeId.indexOf('-')+1), 0)
                    if (src.findChild(sNodeId)) {
                        dNode.remove();
                    }
                }
            });
            // Copy childs recursively
            src.eachChild(function(sNode) {
                var dNodeId = 'category-'+sNode.get('id'),
                    dNode = dst.findChild("id", dNodeId);
                if (!dNode) {
                    var data = Ext.applyIf({
                        id:dNodeId,
                        expanded: true,
                        record: sNode,
                        children: []
                    }, sNode.data);
                    dNode = new WebMailing.model.ItemNode(data);
                    dst.appendChild(dNode);
                } else {
                    dNode.set('record', sNode);
                    dNode.set('title', sNode.get('title'));
                    dNode.set('modified', sNode.get('modified'));
                    dNode.set('created', sNode.get('created'));
                }
                copy_node(sNode, dNode);
            });
        }
        copy_node(this.categories.getRootNode(), this.getRootNode());
    },
    _updateItems: function() {
        // Prune items not present in src
        Ext.each(this.tree.flatten(), function(node) {
            var nodeId = node.get('id');
            if (nodeId && nodeId.indexOf('item-')>-1) {
                var recId = parseInt(nodeId.slice(nodeId.indexOf('-')+1), 0)
                if (!this.items.getById(recId)) {
                    node.remove()
                }
            }
        }, this);
        // Copy items
        var root = this.getRootNode();
        this.items.each(function(item) {
            var itemId = 'item-'+(item.phantom?Ext.id():item.get('id'));
            var data = Ext.applyIf({
                id: itemId,
                leaf:true,
                record: item
            }, item.data);
            var newItem = new WebMailing.model.ItemNode(data);
            var oldItem = root.findChild('id', itemId, true);
            if (oldItem) {
                oldItem.parentNode.replaceChild(newItem, oldItem);
            } else {
                var catId = 'category-'+item.get('category_id');
                var cat=root.findChild('id', catId, true);
                if (cat) {
                    var pos = newItem.get('position');
                    var c = cat;
                    while (c.parentNode) {
                        c.set('position', pos);
                        c = c.parentNode;
                    }
                    cat.appendChild(newItem);
                } else {
                    console.warn('could not find category');
                    return false;
                }
            }
        }, this);
        root.sort(function(a,b) {
            return a.get('position')-b.get('position');
        }, true);
    }
});
