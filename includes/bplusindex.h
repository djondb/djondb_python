// =====================================================================================
// 
//  @file:  bplusindex.h
// 
//  @brief:  This is the definition of the class BPluisIndexP, the implementation of persistent b++ tree
// 
//  @version:  1.0
//  @date:     04/27/2013 09:08:02 PM
//  Compiler:  g++
// 
//  @author:  Juan Pablo Crossley (Cross), crossleyjuan@gmail.com
// 
// This file is part of the djondb project, for license information please refer to the LICENSE file,
// the application and libraries are provided as-is and free of use under the terms explained in the file LICENSE
// Its authors create this application in order to make the world a better place to live, but you should use it on
// your own risks.
// 
// Also, be adviced that, the GPL license force the committers to ensure this application will be free of use, thus
// if you do any modification you will be required to provide it for free unless you use it for personal use (you may 
// charge yourself if you want), bare in mind that you will be required to provide a copy of the license terms that ensures
// this program will be open sourced and all its derivated work will be too.
// =====================================================================================

#ifndef BPLUSINDEX_H
#define BPLUSINDEX_H

#include "index.h"
#include "defs.h"
#include "filterdefs.h"
#include <math.h>
#include <list>

//typedef char* INDEXPOINTERTYPE;
typedef const char* INDEXPOINTERTYPE;

#define INDEXFILEVERSION "0.1.3"

#define COMPAREKEYS(k1, k2) \
	(strcmp(k1, k2) == 0);

//const int BUCKET_MAX_ELEMENTS = 5; // Should be even (3, 5, 7)

class BufferManager;
class MemoryStream;
class Buffer;
class OutputStream;
class BPlusIndex;

void copyArray(void** source, void** destination, int startIndex, int endIndex, int offset);
void removeArray(void** source, int startIndex, int endIndex);

/**
 * @brief This class contains the implementation 
 */
class IndexPage {
	public:
		enum PAGESTATUS {
			NONE,
			LOADED,
			MODIFIED,
			ERASED
		};

		IndexPage(__int32 buckets);
		~IndexPage();

		/**
		 * @brief This contains the elements of the currentpage
		 */
		Index** elements;
		/**
		 * @brief This contains the pointers to other pages that are in between the elements
		 */
		IndexPage** pointers;

		/**
		 * @brief Pointer to the page at the right
		 */
		IndexPage* rightSibling;
		/**
		 * @brief Pointer to the page at the left
		 */
		IndexPage* leftSibling;

		/**
		 * @brief Pointer to the IndexPage that is in top of this IndexPage
		 */
		IndexPage* parentPage;

		void debugElements() const;
		void debug() const;
		bool isLeaf() const;
		bool isFull() const;
		bool _leaf;
		std::list<Index*> find(BufferManager* manager, BaseExpression* filterExpr);
		int findInsertPosition(Index* index) const;
		Index* element(int pos);

		void moveElements(int startPoint, int count);
		void movePointers(int startPoint, int count);

		int maxBuckets() const {
			return _maxBuckets;
		}

		__int32 bufferIndex() const {
			return _bufferIndex;
		}

		void setBufferIndex(__int32 bufferIndex) {
			_bufferIndex = bufferIndex;
		}

		__int32 bufferPos() const {
			return _bufferPos;
		}

		void setBufferPos(__int32 pos) {
			_bufferPos = pos;
		}

		int size;

		/*! \brief Status of the page, used during the persistance
		 * */
		PAGESTATUS status() const {
			return _status;
		}	

		void setStatus(PAGESTATUS status) {
			_status = status;
		}

		void loadPage(BufferManager* manager);

		// refreshes the parent of the child nodes
		void refreshParentRelationship();

#ifndef GTEST_CONTEXT
	private:
#else
	public:
#endif
		__int32 _maxBuckets; 
		__int32 _bufferIndex; /* this contains the index of the buffer where is persisted */
		__int32 _bufferPos; /* This contains the position within the buffer */
		PAGESTATUS _status; /*  Status of the page, this is used during the persistance */
};

/**
 * @brief BPlusIndex implementation, here the BPlusTree is persisted in disc using Buffers
 */
class BPlusIndex: public IndexAlgorithm
{
	public:
		/**
		 * @brief Creates a new Index manager, using the filename and the suggested index size
		 *
		 * @param fileName index file
		 * plus the pointers and the structure.
		 */
		BPlusIndex(const char* fileName);
		virtual ~BPlusIndex();

		/*! \brief This method should be called before using any method in the index
		*/
		void initializeIndex();

		virtual void add(const BSONObj& elem, djondb::string documentId, long filePos);
		virtual bool update(const BSONObj& elem, djondb::string documentId, long filePos);
		virtual Index const* find(BSONObj* const elem);
		virtual bool remove(const BSONObj& elem);
		virtual std::list<Index const*> find(BaseExpression* parser);
		virtual IndexPage* findPage(const BSONObj* key);
		virtual int findElementPos(IndexPage* page, const BSONObj& key);

		void debug();
		virtual void setKeys(std::set<std::string> keys);
		virtual void setIndexName(const char* indexName);
		bool deleteIndex();

		int maxBuckets() const {
			return _maxBuckets;
		}

		void setMaxBuckets(__int32 maxBuckets) {
			if ((maxBuckets % 2) == 0) {
				throw "Only even numbers are allowed";
			}
			_maxBuckets = maxBuckets;
			recalcMidPoint();
		}
		
		void printTreeLEX(const char* name);
		void printBPlus(FILE* out, const char* header);
		FILE* startPrintLEX(const char* name);
		void endPrintLEX(FILE* out);

		/*! \brief This returns the version of the index file
		*/
		virtual Version version() const;
		virtual bool isSupportedVersion(); //!< Each implementation may check if the current version of the file requires recreate because of a change in the format; 
		/*! \brief persist all the pending pages added previously with addPersistQueue
		 * */
#ifndef GTEST_CONTEXT
	private:
#else
	public:
#endif
		IndexPage* _head;
		char* _fileName;
		BufferManager* _bufferManager;

		Index** _tempElements; //<! This is used as a swap area
		IndexPage** _tempPointers; //<! This is used as a swap area

		__int32 _indexPageSize; //<! This is the size for each size, this will be reserved each time a page is persisted

		std::vector<IndexPage*> _persistQueue; //<! This contains the pages that are pending to persist
		__int32 _versionOffset; //<! This contains the position where the information about the head index starts in the control buffer, this enables the file version implementation
		Version* _version; //<! File version
		__int64 _headIndex; //<! Buffer index where the head is stored
		__int64 _headPos; //<! Pos within the buffer index where the head is stored

		__int32 _maxBuckets; //<! Contains how many elements can be on each page
		__int32 _midPoint; //<! Contains the midPoint (ceil of MaxBuckets / 2)

		char* _keysSelect; //<! Preselected keys to be ready to perform select operations on keys

#ifndef GTEST_CONTEXT
	private:
#else
	public:
#endif
		IndexPage* findIndexPage(IndexPage* start, const BSONObj* key);
		Index* findIndex(IndexPage* start, BSONObj* key);
		bool removeIndex(IndexPage* start, const BSONObj& key);
		/*! \brief this deletes the element in the specified position, updating the new size, but nothing else */
		void removeIndexFromPage(IndexPage* page, int pos);
		bool removeIndexFromInner(IndexPage* start, const BSONObj& key);
		bool removeIndexFromLeaf(IndexPage* start, const BSONObj& key);
		void insertIndexElement(IndexPage* page, Index* index);
		void dispose(IndexPage* page);
		void createRoot(Index* element, IndexPage* left, IndexPage* right);
		void addElement(IndexPage* page, Index* element, IndexPage* rightPointer);
		void splitAdd(IndexPage* page, Index* index, IndexPage* rightPointer);
		void splitAddLeaf(IndexPage* page, Index* index);
		void splitAddInner(IndexPage* page, Index* index, IndexPage* rightPointer);

		void collapseRoot();
		void rebalanceTree(IndexPage* changedPage);

		void copyElements(IndexPage* source, IndexPage* destination, int startIndex, int endIndex);
		void removeElements(IndexPage* source, int startIndex, int endIndex);
		void moveElements(IndexPage* source, IndexPage* destination, int startIndex, int endIndex);

		/*! \brief This method identifies if the second objects should be placed to the left or right of the obj1.
		 *
		 * If both elements has an _id then it wont compare the contents, it will use the _id as the sole element to compare.
		 */
		int compareBSON(const BSONObj& obj1, const BSONObj& obj2);

		void recalcMidPoint() {
			_midPoint = ceil((double)_maxBuckets / 2);
		}

		void recalcKeysSelect();
};

#endif // BPLUSINDEX_H
