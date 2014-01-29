#ifndef CONNECTION_H
#define CONNECTION_H

#include <string>
#include <vector>
#include "bson.h"
#include "util.h"
#include "filterparser.h"

#ifdef WINDOWS
   #define LibraryExport   __declspec( dllexport )
#else
   #define LibraryExport
#endif

class NetworkOutputStream;
class NetworkInputStream;
class CommandWriter;
class Transaction;

#define SERVER_PORT 1243

namespace djondb {

    class LibraryExport Connection
    {
        public:
            /** Default constructor */
            Connection(std::string host);
            Connection(std::string host, int port);
            Connection(const Connection& orig);

            /** Default destructor */
            virtual ~Connection();

            bool open();
            void close();
            void internalClose();
            bool isOpen() const;

				bool shutdown() const;

				bool insert(const std::string& db, const std::string& ns, const std::string& json);
            bool insert(const std::string& db, const std::string& ns, const BSONObj& obj);
            BSONObj* findByKey(const std::string& db, const std::string& ns, const std::string& select, const std::string& id);
            BSONObj* findByKey(const std::string& db, const std::string& ns, const std::string& id);
				std::vector<BSONObj*>* find(const std::string& db, const std::string& ns, const std::string& select, const std::string& filter) throw(ParseException);
				std::vector<BSONObj*>* find(const std::string& db, const std::string& ns, const std::string& filter) throw(ParseException);
            bool update(const std::string& db, const std::string& ns, const std::string& json);
            bool update(const std::string& db, const std::string& ns, const BSONObj& bson);

				bool dropNamespace(const std::string& db, const std::string& ns);
				std::vector<std::string>* dbs() const;
				std::vector<std::string>* namespaces(const std::string& db) const;

				std::string host() const;

		  protected:
		  private:
				NetworkOutputStream*  _outputStream;
				NetworkInputStream*   _inputStream;
				CommandWriter*        _commandWriter;

				std::string _host;
				int _port;
				bool _open;
				Logger* _logger;
	 };

}

#endif // CONNECTION_H
