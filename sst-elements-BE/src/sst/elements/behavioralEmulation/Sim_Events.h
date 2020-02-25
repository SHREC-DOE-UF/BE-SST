#ifndef SIM_EVENTS_H
#define SIM_EVENTS_H

#include<sst/core/event.h>
#include <queue>
#include<boost/function.hpp>

namespace SST {
namespace BEComponent {

class simEvent : public SST::Event {

public:
    simEvent() : SST::Event() { }
    
    std::string type;
    double value; // procrastinator!

public:
    void serialize_order(SST::Core::Serialization::serializer &ser) {
        Event::serialize_order(ser);
        ser & type;
        ser & value;
    }

    ImplementSerializable(SST::BEComponent::simEvent);

};
   
     
class changeEvent : public simEvent {
public: 
    changeEvent(std::string attr, std::map<std::string, double> s, double v) : simEvent() { 
        attribute = attr;
        value = v;
        state = s;
        type = "change";
    }        
    
    std::map<std::string, double> state;
    std::string attribute; 

};

 
class conditionEvent : public simEvent {
public: 
    conditionEvent(std::string attr, std::map<std::string, double> s, boost::function<bool(double, double)> cfunc, double v) : simEvent() { 
        attribute = attr;
        value = v;
        state = s;
        conditionFunction = cfunc;
        type = "condition";
    }
    
    std::string attribute;
    boost::function<bool(double, double)> conditionFunction;
    std::map<std::string, double> state;

};


class terminateEvent : public simEvent {
public: 
    terminateEvent() : simEvent() {
        type = "terminate";
    }

};

class waitEvent : public simEvent {
public: 
    waitEvent() : simEvent() {
        type = "wait";
    }

};

class ackEvent : public simEvent {
public: 
    ackEvent(int pi, std::vector<int> loc, int nh) : simEvent() {
        type = "acknowledge";
        locations = loc;
        pid = pi;
        next_hop = nh;
    }

    std::vector<int> locations;
    int pid, next_hop;

};

class timeoutEvent : public simEvent {
public: 
    timeoutEvent(double v) : simEvent() { 
        value = v;    
        type = "timeout";
    }
	
};

class commEvent : public simEvent {
public: 
    commEvent(int pi, int so, int si, int rk, int tg, std::vector<int> tlist, std::vector<int> loc, int nh, std::string ct) : simEvent() { 
        source = so;
        size = si;
        target = rk;
        tag = tg;
        locations = loc;
        tarlist = tlist;
        next_hop = nh;
        comm_type = ct;
        pid = pi;   
        type = "initiate communication";
    }

    int pid, source, size, target, tag, next_hop;
    std::string comm_type; 
    std::vector<int> locations, tarlist;
	
};

class recvEvent : public simEvent {
public: 
    recvEvent() : simEvent() {
        type = "receive";
    }

}; 

class recvWaitEvent : public simEvent {
public: 
    recvWaitEvent() : simEvent() {
        type = "receiveWait";
    }

};

class callEvent : public simEvent {	
public:
    callEvent(int sg, int spid, int trg, std::string tar, std::string ops, std::vector<float> ips, std::string ct) : simEvent() {
        source_gid = sg;
        source_pid = spid;
        target_gid = trg;
        target_family = tar;
        operation = ops;
        inputs = ips;
        call_type = ct;
        type = "call";
    }

    int source_gid, source_pid, target_gid;
    std::string target_family, operation, call_type;
    std::vector<float> inputs;

};     

class barrierEvent : public simEvent {
public:
    barrierEvent(int so, int grp) : simEvent() {
	source = so;
        commgroup = grp;
        type = "barrier";
    }

    int source, commgroup;

};     

class routeEvent : public simEvent {
public: 
    routeEvent(int g, int p, int so, int tar, std::vector<int> loc) : simEvent() { 
        gid = g;
        pid = p;
        source = so;
        target = tar;
        locations = loc;   
        type = "route";
    }

    int gid, pid, source, target;
    std::vector<int> locations;
	
};            


}
}

#endif
  
