#ifndef CONNECTIONMANAGER_H
#define CONNECTIONMANAGER_H

#include <map>
#include <string>
#include "util.h"

#ifdef WINDOWS
   #define LibraryExport   __declspec( dllexport )
#else
   #define LibraryExport
#endif


namespace djondb {
    class Connection;

    struct ConnectionReference {
        Connection* _connection;
        int _references;
    };

    class LibraryExport ConnectionManager
    {
        public:
            /** Default constructor */
            ConnectionManager();
            /** Default destructor */
            virtual ~ConnectionManager();

            static Connection* getConnection(std::string host);
            static Connection* getConnection(std::string host, int port);

            static void releaseConnection(Connection* conn);

        protected:
        private:
            static std::map<std::string, struct ConnectionReference> _connections;

			static bool __initialized;
    };
}

#endif // CONNECTIONMANAGER_H
